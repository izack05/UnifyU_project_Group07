"""Add balance column to StudentRegistration

Revision ID: b0bfaf6a8359
Revises: bcc2f4e41efa
Create Date: 2025-08-25 05:48:33.500610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0bfaf6a8359'
down_revision = 'bcc2f4e41efa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'student_registration',
        sa.Column('balance', sa.Integer(), nullable=False, server_default='0')
    )


def downgrade():
    op.drop_column('student_registration', 'balance')
