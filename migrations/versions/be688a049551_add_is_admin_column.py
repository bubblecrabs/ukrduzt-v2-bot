"""add is_admin column

Revision ID: be688a049551
Revises: 3bbd7eeef9c7
Create Date: 2025-02-07 16:17:48.979305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be688a049551'
down_revision: Union[str, None] = '3bbd7eeef9c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.create_index('ix_users_is_admin', 'users', ['is_admin'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_users_is_admin', table_name='users')
    op.drop_column('users', 'is_admin')
