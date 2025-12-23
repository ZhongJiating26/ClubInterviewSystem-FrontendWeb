from sqlmodel import Session

from app.db.session import engine
from app.repositories.user_account import UserAccountRepository


def main():
    repo = UserAccountRepository()

    with Session(engine) as session:
        # 1) 注册
        user = repo.create_user(
            session,
            phone="13800000001",
            password="123456",
            name="测试用户",
        )
        print("created user id:", user.id)

        # 2) 按手机号查
        user2 = repo.get_by_phone(session, "13800000001")
        print("found user:", user2.id, user2.phone)

        # 3) 验证密码
        ok = repo.verify_password("123456", user2.password_hash)
        print("password verify:", ok)


if __name__ == "__main__":
    main()
