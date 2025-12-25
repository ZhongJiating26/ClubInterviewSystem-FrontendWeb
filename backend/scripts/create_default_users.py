#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建预制账号脚本
用于创建普通学生账号和系统管理员账号
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session
from app.db.session import get_session
from app.repositories.user_account import UserAccountRepository
from app.models.user_account import UserAccount
from app.models.role import Role, UserRole
from app.repositories.role import RoleRepository, UserRoleRepository
from sqlmodel import select


def create_default_users():
    """创建预制账号"""
    session: Session = next(get_session())
    user_repo = UserAccountRepository()
    role_repo = RoleRepository()
    user_role_repo = UserRoleRepository()
    
    try:
        # 1. 创建普通学生账号
        print("正在创建普通学生账号...")
        student_phone = "13800000001"
        student_password = "student123"
        student_name = "张三"
        
        # 检查是否已存在
        existing_student = user_repo.get_by_phone(session, student_phone)
        if existing_student:
            print(f"普通学生账号已存在: {student_phone}")
        else:
            student = user_repo.create_user(
                session,
                phone=student_phone,
                password=student_password,
                name=student_name,
                school_id=None,
            )
            print(f"✓ 普通学生账号创建成功")
            print(f"  手机号: {student_phone}")
            print(f"  密码: {student_password}")
            print(f"  姓名: {student_name}")
            print(f"  用户ID: {student.id}")
        
        # 2. 创建系统管理员账号
        print("\n正在创建系统管理员账号...")
        admin_phone = "13800000000"
        admin_password = "admin123"
        admin_name = "系统管理员"
        
        # 检查是否已存在
        existing_admin = user_repo.get_by_phone(session, admin_phone)
        if existing_admin:
            print(f"系统管理员账号已存在: {admin_phone}")
            admin = existing_admin
        else:
            admin = user_repo.create_user(
                session,
                phone=admin_phone,
                password=admin_password,
                name=admin_name,
                school_id=None,
            )
            print(f"✓ 系统管理员账号创建成功")
            print(f"  手机号: {admin_phone}")
            print(f"  密码: {admin_password}")
            print(f"  姓名: {admin_name}")
            print(f"  用户ID: {admin.id}")
        
        # 3. 创建管理员角色（如果不存在）
        print("\n正在创建管理员角色...")
        admin_role = role_repo.get_by_code(session, "admin")
        if not admin_role:
            admin_role = Role(
                name="系统管理员",
                code="admin",
                description="系统管理员，拥有所有权限",
                status=1,
            )
            admin_role = role_repo.create(session, admin_role)
            print(f"✓ 管理员角色创建成功 (ID: {admin_role.id})")
        else:
            print(f"管理员角色已存在 (ID: {admin_role.id})")
        
        # 4. 为管理员账号分配角色
        print("\n正在为管理员分配角色...")
        # 检查是否已分配角色
        stmt = (
            select(UserRole)
            .where(UserRole.user_id == admin.id)
            .where(UserRole.role_id == admin_role.id)
            .where(UserRole.is_deleted == 0)
        )
        existing_user_role = session.exec(stmt).first()
        if not existing_user_role:
            user_role = UserRole(
                user_id=admin.id,
                role_id=admin_role.id,
                status=1,
            )
            user_role_repo.create(session, user_role)
            print(f"✓ 管理员角色分配成功")
        else:
            print(f"管理员角色已分配")
        
        session.commit()
        print("\n" + "="*50)
        print("预制账号创建完成！")
        print("="*50)
        print("\n账号信息：")
        print("\n【普通学生账号】")
        print(f"  手机号: {student_phone}")
        print(f"  密码: {student_password}")
        print(f"  姓名: {student_name}")
        print(f"  角色: 普通学生")
        
        print("\n【系统管理员账号】")
        print(f"  手机号: {admin_phone}")
        print(f"  密码: {admin_password}")
        print(f"  姓名: {admin_name}")
        print(f"  角色: 系统管理员")
        print("\n提示：请妥善保管这些账号信息，生产环境请及时修改密码！")
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ 创建失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    create_default_users()

