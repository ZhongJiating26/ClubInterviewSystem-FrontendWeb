from typing import Optional
import bcrypt

from sqlmodel import Session, select
from passlib.context import CryptContext

from app.models.user_account import UserAccount
from app.repositories.base import BaseRepository


# 密码哈希工具（bcrypt）
# 使用 bcrypt 的 rounds=12，与 passlib 默认一致
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)


class UserAccountRepository(BaseRepository[UserAccount]):
    """
    用户账号仓储
    """

    def __init__(self):
        super().__init__(UserAccount)

    # ========= 密码相关 =========

    def _ensure_password_bytes(self, password: str) -> bytes:
        """
        确保密码字节长度不超过 72 字节（bcrypt 限制）
        返回截断后的字节
        """
        if not password:
            return b''
        
        password_bytes = password.encode('utf-8')
        if len(password_bytes) <= 72:
            return password_bytes
        
        # 截断到 72 字节
        truncated_bytes = password_bytes[:72]
        
        # 移除末尾可能不完整的 UTF-8 字符
        # UTF-8 多字节字符的后续字节以 10xxxxxx 开头
        while len(truncated_bytes) > 0 and (truncated_bytes[-1] & 0b11000000) == 0b10000000:
            truncated_bytes = truncated_bytes[:-1]
        
        return truncated_bytes

    def hash_password(self, raw_password: str) -> str:
        """
        哈希密码
        bcrypt 限制密码最多 72 字节，直接使用 bcrypt 库确保截断
        """
        if not raw_password:
            raise ValueError("密码不能为空")
        
        # 确保密码字节不超过 72 字节
        password_bytes = self._ensure_password_bytes(raw_password)
        
        # 直接使用 bcrypt 库，避免 passlib 的内部问题
        # bcrypt.hashpw 接受 bytes，自动处理 72 字节限制
        salt = bcrypt.gensalt(rounds=12)
        password_hash_bytes = bcrypt.hashpw(password_bytes, salt)
        
        # 将 bytes 解码为字符串存储
        return password_hash_bytes.decode('utf-8')

    def verify_password(self, raw_password: str, password_hash: str) -> bool:
        """
        验证密码
        需要与 hash_password 使用相同的截断逻辑
        """
        if not raw_password or not password_hash:
            return False
        
        # 使用相同的截断逻辑
        password_bytes = self._ensure_password_bytes(raw_password)
        
        # 将存储的哈希字符串编码为 bytes
        password_hash_bytes = password_hash.encode('utf-8')
        
        # 直接使用 bcrypt 库验证
        try:
            return bcrypt.checkpw(password_bytes, password_hash_bytes)
        except (ValueError, TypeError):
            # 如果验证失败（可能是旧格式的哈希），尝试使用 passlib 验证
            # 这用于向后兼容
            try:
                return pwd_context.verify(raw_password, password_hash)
            except Exception:
                return False

    # ========= 查询 =========

    def get_by_phone(self, session: Session, phone: str) -> Optional[UserAccount]:
        """
        根据手机号查询未删除用户
        """
        stmt = (
            select(UserAccount)
            .where(UserAccount.phone == phone)
            .where(UserAccount.is_deleted == 0)
        )
        return session.exec(stmt).first()

    # ========= 创建用户（注册核心） =========

    def create_user(
        self,
        session: Session,
        *,
        phone: str,
        password: str,
        name: Optional[str] = None,
        school_id: Optional[int] = None,
    ) -> UserAccount:
        """
        创建新用户（自动 hash 密码）
        """
        password_hash = self.hash_password(password)

        user = UserAccount(
            phone=phone,
            password_hash=password_hash,
            name=name,
            school_id=school_id,
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    #查询ID

    def get_by_id(self, session: Session, user_id: int) -> Optional[UserAccount]:
        """
        根据 ID 查询未删除用户
        """
        stmt = (
            select(UserAccount)
            .where(UserAccount.id == user_id)
            .where(UserAccount.is_deleted == 0)
        )
        return session.exec(stmt).first()

    def init_account(
            self,
            session: Session,
            *,
            user: UserAccount,
            password: str,
            name: str,
            id_card_no: str,
            school_id: int,
            major: str,
            student_no: str,
            email: Optional[str] = None,
            avatar_url: Optional[str] = None,
    ) -> UserAccount:
        """
        账号初始化：设置密码 + 补全资料
        注意：这里不做权限判断（是否允许初始化），权限判断放在 API 层
        """
        user.password_hash = self.hash_password(password)
        user.name = name
        user.id_card_no = id_card_no
        user.school_id = school_id
        user.major = major
        user.student_no = student_no
        user.email = email
        user.avatar_url = avatar_url

        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def change_password(
        self,
        session: Session,
        *,
        user: UserAccount,
        old_password: str,
        new_password: str,
    ) -> UserAccount:
        """
        修改密码：
        1. 验证旧密码
        2. 设置新密码
        3. 增加 token_version（使所有旧token失效）
        """
        # 1. 验证旧密码
        if not self.verify_password(old_password, user.password_hash):
            raise ValueError("旧密码错误")

        # 2. 设置新密码
        user.password_hash = self.hash_password(new_password)

        # 3. 增加 token_version（使所有旧token失效）
        user.token_version += 1

        user.touch()
        session.add(user)
        session.commit()
        session.refresh(user)
        return user