"""create user table

Revision ID: 2d40a1ad1466
Revises: 
Create Date: 2021-04-23 12:19:36.960214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d40a1ad1466'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('token', sa.String(255), nullable=False))


def downgrade():
    op.drop_table('user')
