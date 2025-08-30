revision = 'add_cancelled_status_to_order'
down_revision = '351b07875ca8'
branch_labels = None
depends_on = None
"""
Revision script to add 'Cancelled' as a possible value for the 'status' column in the 'order' table.
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # No schema change needed, but this migration documents the new status value
    pass

def downgrade():
    pass
