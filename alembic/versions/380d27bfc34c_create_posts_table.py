"""create posts table

Revision ID: 380d27bfc34c
Revises: 
Create Date: 2026-04-23 11:38:18.262159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '380d27bfc34c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # """Upgrade schema."""
    op.create_table(
        'orm_posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String, nullable=False)
    )
    pass


def downgrade() -> None:
    # """Downgrade schema."""
    op.drop_table('orm_posts', if_exists=True)
