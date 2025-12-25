"""make password_hash nullable

Revision ID: 7d2920a07a59
Revises: 9e13212a1495
Create Date: 2025-12-24 00:10:28.734768

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7d2920a07a59'
down_revision: Union[str, Sequence[str], None] = '9e13212a1495'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite 不支持直接 ALTER COLUMN，需要使用 batch mode
    # 但由于 password_hash 在创建时已经是 nullable=False，我们需要重新创建表
    # 为了简化，我们使用 batch_alter_table（如果可用）或者直接跳过
    # 实际上，由于 SQLite 的限制，这个迁移在 SQLite 中可能无法执行
    # 建议：在创建表时就设置 password_hash 为 nullable=True
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
                            existing_type=sa.String(length=255),
                            nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
                            existing_type=sa.String(length=255),
                            nullable=False)
    # ### end Alembic commands ###
