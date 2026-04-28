"""new fields in user model

Revision ID: 37f06a334dbf
Revises: 780739b227a7
Create Date: 2026-04-28 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "37f06a334dbf"
down_revision = "780739b227a7"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("about_me", sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column("last_seen", sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("last_seen")
        batch_op.drop_column("about_me")
