"""add content column

Revision ID: e09466a5ed25
Revises: 380d27bfc34c
Create Date: 2026-04-23 12:11:15.637221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e09466a5ed25'
down_revision: Union[str, Sequence[str], None] = '380d27bfc34c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # """Upgrade schema."""
    op.add_column('orm_posts', sa.Column('content', sa.String, nullable=False))


def downgrade() -> None:
    # """Downgrade schema."""
    op.drop_column('orm_posts', 'content', if_exists=True)
