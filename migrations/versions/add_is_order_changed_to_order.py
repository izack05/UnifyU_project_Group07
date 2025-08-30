revision = 'add_is_order_changed_to_order'
down_revision = '351b07875ca8'
branch_labels = None
depends_on = None
"""
Add is_order_changed column to order table for student notification tracking.
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('order', sa.Column('is_order_changed', sa.Boolean(), nullable=False, server_default=sa.false()))

def downgrade():
    op.drop_column('order', 'is_order_changed')
