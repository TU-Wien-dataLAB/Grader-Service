"""Settings column

Revision ID: 4620c13728e7
Revises: a1791b1371ed
Create Date: 2023-09-11 15:46:57.162396

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4620c13728e7'
down_revision = 'a1791b1371ed'
branch_labels = None
depends_on = None


def upgrade():
    # use settings to save arbitrary json
    op.add_column('assignment', sa.Column('settings', sa.Text, server_default='{}', nullable=False))

    # columns for original points (grading_points) and the late submission scaling (point_scaling)
    op.add_column('submission', sa.Column('grading_score', sa.DECIMAL(10, 3), nullable=False))
    op.add_column('submission', sa.Column('score_scaling', sa.DECIMAL(10, 3), server_default="1.0", nullable=False))


def downgrade():
    op.drop_column('assignment', 'settings')
    op.drop_column('submission', 'grading_points')
    op.drop_column('submission', 'point_scaling')
