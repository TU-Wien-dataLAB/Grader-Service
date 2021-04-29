"""create assignment table

Revision ID: a4d3c8697d25
Revises: cec39fe7741d
Create Date: 2021-04-23 12:21:42.095845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4d3c8697d25'
down_revision = 'cec39fe7741d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('assignment',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name',sa.String(255), nullable=False),
        sa.Column('lectid', sa.Integer, sa.ForeignKey('lecture.id')),
        sa.Column('duedate', sa.DateTime, nullable=False),
        sa.Column('path', sa.String(255), nullable=False),
        sa.Column('points', sa.Integer, nullable=False),
        sa.Column('status', sa.Enum('created', 'released', 'fetching', 'fetched', 'complete'), default='created')
        )

        # op.create_table('assignment',
        #sa.Column('id', sa.Integer, primary_key=True),
        #sa.Column(),
        #sa.Column())


def downgrade():
    op.drop_table('assignment')
