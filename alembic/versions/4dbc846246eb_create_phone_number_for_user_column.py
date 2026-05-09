"""Create phone number for user column

Revision ID: 4dbc846246eb
Revises: 
Create Date: 2026-04-07 00:14:26.150267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dbc846246eb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('', sa.Column('phone_number', sa.String(), nullable=True))
    """Upgrade schema."""



def downgrade() -> None:
    op.drop_column('users', 'phone_number')
    """Downgrade schema."""

