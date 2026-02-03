"""Create phone for user column

Revision ID: b9fa4699b4d8
Revises: 
Create Date: 2026-02-03 10:47:20.383226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9fa4699b4d8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
