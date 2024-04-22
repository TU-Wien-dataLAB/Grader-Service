"""Added oauth provider functionality

Revision ID: ba71c755c153
Revises: 9cfeb0faa0c0
Create Date: 2023-08-18 10:30:24.465356

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Unicode, Integer, DateTime, Text, \
    PrimaryKeyConstraint, ForeignKeyConstraint

# revision identifiers, used by Alembic.
revision = 'ba71c755c153'
down_revision = '9cfeb0faa0c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('api_token',
                    Column('username', Unicode(255)),
                    Column('id', Integer, nullable=True),
                    Column('hashed', Unicode(255)),
                    Column('prefix', Unicode(16)),
                    Column('client_id', Unicode(255)),
                    Column('session_id', Unicode(255)),
                    Column('created', DateTime),
                    Column('expires_at', DateTime),
                    Column('last_activity', DateTime),
                    Column('note', Unicode(1023)),
                    Column('scopes', Text),
                    PrimaryKeyConstraint('id'),
                    ForeignKeyConstraint(['username'], ['user.name'])
                    )

    op.create_table('oauth_client',
                    Column('id', Integer, nullable=True),
                    Column('identifier', Unicode(255), unique=True),
                    Column('description', Unicode(1023)),
                    Column('secret', Unicode(255)),
                    Column('redirect_uri', Unicode(1023)),
                    Column('allowed_scopes', Text),
                    PrimaryKeyConstraint('id')
                    )

    op.create_table('oauth_code',
                    Column('id', Integer, nullable=True),
                    Column('client_id', Unicode(255)),
                    Column('code', Unicode(36)),
                    Column('expires_at', Integer),
                    Column('redirect_uri', Unicode(1023)),
                    Column('username', Unicode(255)),
                    Column('scopes', Text),
                    PrimaryKeyConstraint("id"),
                    ForeignKeyConstraint(['client_id'],
                                         ['oauth_client.identifier']),
                    ForeignKeyConstraint(['username'], ['user.name'])
                    )


def downgrade():
    op.drop_table('api_token')
    op.drop_table('oauth_code')
    op.drop_table('oauth_client')
