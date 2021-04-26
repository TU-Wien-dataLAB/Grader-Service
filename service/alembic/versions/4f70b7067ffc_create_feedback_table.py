"""create feedback table

Revision ID: 4f70b7067ffc
Revises: 590686a48639
Create Date: 2021-04-23 12:22:27.411385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f70b7067ffc'
down_revision = '590686a48639'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('feedback',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('score', sa.Integer, nullable=False),
        )



def downgrade():
    op.drop_table('feedback')
