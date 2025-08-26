"""drop and recreate clubapp

Revision ID: 17ba6aa7880e
Revises: 62e6febfc294
Create Date: 2025-08-26 22:28:57.530153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17ba6aa7880e'
down_revision = '62e6febfc294'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("clubapp")


def downgrade():
    op.create_table(
        "clubapp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("studid", sa.Integer, nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("phone", sa.Integer, nullable=False),
        sa.Column("name", sa.String(500), nullable=False),
        sa.Column("interests", sa.String(500), nullable=False),
        sa.Column("skills", sa.String(500), nullable=False),
        sa.Column("club_id", sa.Integer, sa.ForeignKey("club.id"), nullable=False),
    )
