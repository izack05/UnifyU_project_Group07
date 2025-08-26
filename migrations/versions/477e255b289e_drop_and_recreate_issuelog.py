"""drop and recreate IssueLog

Revision ID: 477e255b289e
Revises: 154343580498
Create Date: 2025-08-27 02:16:02.963688

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '477e255b289e'
down_revision = '154343580498'
branch_labels = None
depends_on = None


def upgrade():
    # Drop the existing table
    op.drop_table("issue_log")

    # Recreate it with the updated schema
    op.create_table(
        "issue_log",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("student_registration.id", name="fk_issue_log_student"), nullable=False),
        sa.Column("resolved_by", sa.Integer, sa.ForeignKey("student_registration.id", name="fk_issue_log_resolved_by"), nullable=True),
        sa.Column("issue_title", sa.String(200), nullable=False),
        sa.Column("issue_category", sa.String(50), nullable=False),
        sa.Column("issue_description", sa.Text, nullable=False),
        sa.Column("floor", sa.String(3), nullable=False, default="1"),
        sa.Column("location", sa.String(100), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False, default="Medium"),
        sa.Column("status", sa.String(20), nullable=False, default="Reported"),
        sa.Column("submitted_at", sa.DateTime, nullable=False, default=datetime.now),
        sa.Column("resolved_at", sa.DateTime, nullable=True),
        sa.Column("staff_notes", sa.Text, nullable=True),
        sa.Column("is_new", sa.Boolean, nullable=False, default=True)
    )


def downgrade():
    # Drop the table if rolling back
    op.drop_table("issue_log")
