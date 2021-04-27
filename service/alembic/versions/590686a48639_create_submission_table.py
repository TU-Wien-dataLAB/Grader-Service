"""create submission table

Revision ID: 590686a48639
Revises: ae5bd6cbf435
Create Date: 2021-04-23 12:22:13.198728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '590686a48639'
down_revision = 'ae5bd6cbf435'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('submission',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name',sa.String(255), nullable=False),
        sa.Column('lectid', sa.Integer, sa.ForeignKey('lecture.id')),
        sa.Column('duedate', sa.DateTime, nullable=False),
        sa.Column('path', sa.String(255), nullable=False),
        sa.Column('points', sa.Integer, nullable=False)
        )

        # op.create_table('assignment',
        #sa.Column('id', sa.Integer, primary_key=True),
        #sa.Column(),
        #sa.Column())


def downgrade():
    op.drop_table('submission')
