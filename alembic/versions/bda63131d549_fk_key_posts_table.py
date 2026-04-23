"""fk_key posts table

Revision ID: bda63131d549
Revises: 670d7b9a1a0f
Create Date: 2026-04-23 12:48:12.219683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bda63131d549'
down_revision: Union[str, Sequence[str], None] = '670d7b9a1a0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # """Upgrade schema."""
    op.add_column('orm_posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk", source_table="orm_posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    # """Downgrade schema."""
    op.drop_constraint("posts_users_fk", table_name="orm_posts", type_="foreignkey", if_exists=True)
    op.drop_column('orm_posts', 'owner_id', if_exists=True)
    pass
