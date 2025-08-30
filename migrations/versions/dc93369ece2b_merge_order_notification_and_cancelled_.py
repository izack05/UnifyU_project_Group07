"""merge order notification and cancelled status branches

Revision ID: dc93369ece2b
Revises: add_cancelled_status_to_order, add_is_order_changed_to_order
Create Date: 2025-08-30 05:03:45.357387

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc93369ece2b'
down_revision = ('add_cancelled_status_to_order', 'add_is_order_changed_to_order')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
