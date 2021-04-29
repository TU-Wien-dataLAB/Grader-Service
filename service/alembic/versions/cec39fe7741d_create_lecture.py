"""create lecture

Revision ID: cec39fe7741d
Revises: 2d40a1ad1466
Create Date: 2021-04-23 12:21:04.302329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cec39fe7741d'
down_revision = '2d40a1ad1466'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('lecture',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name',sa.String(255), nullable=False, unique=True),
        sa.Column('semester',sa.String(255), nullable=False),
        sa.Column('code', sa.String(255), nullable=False),
        sa.Column('complete',sa.Boolean(), default=False))


def downgrade():
    op.drop_table('lecture')
