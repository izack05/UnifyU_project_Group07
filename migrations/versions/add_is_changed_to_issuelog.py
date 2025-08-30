"""add is_changed column to IssueLog for student notifications
Revision ID: add_is_changed_to_issuelog
Revises: 846b1ee2c131
Create Date: 2025-08-30
"""

revision = 'add_is_changed_to_issuelog'
down_revision = '846b1ee2c131'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    with op.batch_alter_table('issue_log', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_changed', sa.Boolean(), nullable=False, server_default=sa.false()))

def downgrade():
    with op.batch_alter_table('issue_log', schema=None) as batch_op:
        batch_op.drop_column('is_changed')
