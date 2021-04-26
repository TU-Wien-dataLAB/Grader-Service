"""create file table

Revision ID: ae5bd6cbf435
Revises: a4d3c8697d25
Create Date: 2021-04-23 12:22:01.396997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae5bd6cbf435'
down_revision = 'a4d3c8697d25'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('file',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('assignid', sa.Integer, sa.ForeignKey('assignment.id')),
        sa.Column('path', sa.String(255), nullable=False),
        sa.Column('exercise', sa.Boolean, nullable=False),                
        sa.Column('points', sa.Integer),
        )


def downgrade():
    op.drop_table('file')
