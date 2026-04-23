"""post table

Revision ID: 39342041c719
Revises: e09466a5ed25
Create Date: 2026-04-23 12:33:10.646438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39342041c719'
down_revision: Union[str, Sequence[str], None] = 'e09466a5ed25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # """Upgrade schema."""
    op.add_column('orm_posts', sa.Column('published', sa.Boolean, server_default='True', nullable=False))
    op.add_column('orm_posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    # """Downgrade schema."""
    op.drop_column('orm_posts', 'published', if_exists=True)
    op.drop_column('orm_posts', 'created_at', if_exists=True)

    pass
