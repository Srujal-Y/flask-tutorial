"""make email nullable

Revision ID: a1b2c3d4e5f6
Revises: 834b1a697901
Create Date: 2025-05-11 06:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '834b1a697901'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
                              existing_type=sa.String(length=120),
                              nullable=True)


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
                              existing_type=sa.String(length=120),
                              nullable=False)
