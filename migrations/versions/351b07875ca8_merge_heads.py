"""merge heads

Revision ID: 351b07875ca8
Revises: 477e255b289e, add_is_changed_to_issuelog
Create Date: 2025-08-30 01:32:14.706064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '351b07875ca8'
down_revision = ('477e255b289e', 'add_is_changed_to_issuelog')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
