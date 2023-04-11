# Copyright (c) 2022, TU Wien
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""initial

Revision ID: a1791b1371ed
Revises: 
Create Date: 2021-05-05 11:42:24.126371

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import UniqueConstraint

# revision identifiers, used by Alembic.
revision = 'a1791b1371ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lecture',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),

                    sa.Column('name', sa.String(length=255), nullable=True),

                    sa.Column('code', sa.String(length=255),
                              nullable=True, unique=True),

                    sa.Column('state', sa.Enum('active', 'complete',
                                               name='lecture_state'),
                              nullable=False),

                    sa.Column('deleted', sa.Enum('active', 'deleted',
                                                 name='deleted'),
                              server_default='active',
                              nullable=False),

                    sa.Column('created_at', sa.DateTime(),
                              default=datetime.utcnow, nullable=False),

                    sa.Column('updated_at', sa.DateTime(),
                              default=datetime.utcnow,
                              onupdate=datetime.utcnow,
                              nullable=False),

                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('user',
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('name')
                    )

    op.create_table('assignment',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),

                    sa.Column('name', sa.String(length=255), nullable=False),

                    sa.Column('type', sa.Enum("user", "group",
                                              name='assignment_type'),
                              nullable=False,
                              server_default="user"),

                    sa.Column('lectid', sa.Integer(), nullable=True),

                    sa.Column('duedate', sa.DateTime(), nullable=True),

                    sa.Column('automatic_grading',
                              sa.Enum('unassisted', 'auto',
                                      'full_auto', name='automatic_grading'),
                              server_default='unassisted', nullable=False),

                    sa.Column('points', sa.DECIMAL(10, 3), nullable=False),

                    sa.Column('status',
                              sa.Enum('created', 'pushed', 'released',
                                      'fetching', 'fetched', 'complete',
                                      name='assignment_status'),
                              nullable=True),

                    sa.Column('deleted',
                              sa.Enum('active', 'deleted', name='deleted'),
                              server_default='active',
                              nullable=False),

                    sa.Column('max_submissions', sa.Integer(),
                              nullable=True, default=None, unique=False),

                    sa.Column('allow_files', sa.Boolean(),
                              nullable=False, default=False),
                    sa.Column('properties', sa.Text(),
                              nullable=True, unique=False),

                    sa.Column('created_at', sa.DateTime(),
                              default=datetime.utcnow, nullable=False),

                    sa.Column('updated_at', sa.DateTime(),
                              default=datetime.utcnow,
                              onupdate=datetime.utcnow,
                              nullable=False),

                    sa.ForeignKeyConstraint(['lectid'],
                                            ['lecture.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    UniqueConstraint('name', 'lectid',
                                     'deleted', name='u_name_in_lect')
                    )

    op.create_table('takepart',
                    sa.Column('username', sa.String(length=255),
                              nullable=False),
                    sa.Column('lectid', sa.Integer(), nullable=False),
                    sa.Column('role', sa.String(length=255), nullable=False),
                    sa.ForeignKeyConstraint(['lectid'], ['lecture.id'], ),
                    sa.ForeignKeyConstraint(['username'], ['user.name'], ),
                    sa.PrimaryKeyConstraint('username', 'lectid')
                    )

    op.create_table('group',
                    sa.Column('id', sa.Integer(), autoincrement=True),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('lectid', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['lectid'], ['lecture.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('partof',
                    sa.Column('username', sa.String(length=255), nullable=False),
                    sa.Column('group_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
                    sa.ForeignKeyConstraint(['username'], ['user.name'], ),
                    sa.PrimaryKeyConstraint('username', 'group_id')
                    )

    op.create_table('submission',
                    sa.Column('id', sa.Integer(), autoincrement=True,
                              nullable=False),

                    sa.Column('date', sa.DateTime(), nullable=True),

                    sa.Column('auto_status',
                              sa.Enum('pending', 'not_graded',
                                      'automatically_graded',
                                      'grading_failed', name='auto_status'),
                              nullable=False),

                    sa.Column('manual_status',
                              sa.Enum('not_graded', 'manually_graded',
                                      'being_edited', name='manual_status'),
                              nullable=False),

                    sa.Column('edited', sa.Boolean(), default=False),

                    sa.Column('score', sa.DECIMAL(10, 3), nullable=True),

                    sa.Column('assignid', sa.Integer(), nullable=True),

                    sa.Column('username', sa.String(length=255),
                              nullable=True),

                    sa.Column('commit_hash', sa.String(length=40),
                              nullable=False),

                    sa.Column('feedback_available', sa.Boolean(),
                              nullable=False, server_default="false"),

                    sa.Column('updated_at', sa.DateTime(),
                              default=datetime.utcnow,
                              onupdate=datetime.utcnow,
                              nullable=False),

                    sa.ForeignKeyConstraint(['assignid'], ['assignment.id'], ),
                    sa.ForeignKeyConstraint(['username'], ['user.name'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('submission_logs',
                    sa.Column('sub_id', sa.Integer(), nullable=False),

                    sa.Column('logs', sa.Text(), nullable=True),

                    sa.ForeignKeyConstraint(['sub_id'], ['submission.id'], ),
                    sa.PrimaryKeyConstraint('sub_id')
                    )

    op.create_table('submission_properties',
                    sa.Column('sub_id', sa.Integer(), nullable=False),

                    sa.Column('properties', sa.Text(),
                              nullable=True, unique=False),

                    sa.ForeignKeyConstraint(['sub_id'], ['submission.id'], ),
                    sa.PrimaryKeyConstraint('sub_id')
                    )

    # ### end Alembic commands ###


def downgrade():
    # This does not drop enum types which are required when using postgresql
    op.drop_table('submission_logs')
    op.drop_table('submission_properties')
    op.drop_table('submission')
    op.drop_table('takepart')
    op.drop_table('assignment')
    op.drop_table('partof')
    op.drop_table('group')
    op.drop_table('lecture')
    op.drop_table('user')
    # ### end Alembic commands ###
