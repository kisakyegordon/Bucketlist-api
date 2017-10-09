"""empty message

Revision ID: 2f900efad48b
Revises: 67f283c338d6
Create Date: 2017-10-05 14:04:57.335984

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f900efad48b'
down_revision = '67f283c338d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('bucketlists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Bucketlistitems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=255), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('bucketlist_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bucketlist_id'], ['bucketlists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Bucketlistitems')
    op.drop_table('bucketlists')
    op.drop_table('users')
    # ### end Alembic commands ###
