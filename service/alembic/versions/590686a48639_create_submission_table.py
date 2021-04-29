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
        sa.Column('date', sa.DateTime, nullable=False),
        sa.Column('assignid', sa.Integer, sa.ForeignKey('assignment.id')),
        sa.Column('username', sa.Integer, sa.ForeignKey('user.name'))
        )


def downgrade():
    op.drop_table('submission')
