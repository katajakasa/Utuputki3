"""Initial models

Revision ID: 6bb8cf7ee4e7
Revises: 
Create Date: 2016-11-27 04:15:53.076554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bb8cf7ee4e7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'test',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('value', sa.Unicode(length=36), nullable=False),
        sa.PrimaryKeyConstraint('id', name='test_id_pkey')
    )
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.Unicode(length=32), nullable=False),
        sa.Column('password', sa.Unicode(length=32), nullable=False),
        sa.Column('nickname', sa.Unicode(length=32), nullable=False),
        sa.Column('email', sa.Unicode(length=128), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id', name='user_id_pkey'),
        sa.UniqueConstraint('username')
    )


def downgrade():
    op.drop_table('user')
    op.drop_table('test')
