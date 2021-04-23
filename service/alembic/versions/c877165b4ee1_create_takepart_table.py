"""create takepart table

Revision ID: c877165b4ee1
Revises: 4f70b7067ffc
Create Date: 2021-04-23 12:22:37.418006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c877165b4ee1'
down_revision = '4f70b7067ffc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('takepart',
        sa.Column('userid', sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
        sa.Column('lectid', sa.Integer, sa.ForeignKey('lecture.id'), primary_key=True),
        sa.Column('role', sa.String(255), nullable=False)
        )


def downgrade():
    op.drop_table('takepart')

