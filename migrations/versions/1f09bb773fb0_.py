"""empty message

Revision ID: 1f09bb773fb0
Revises: 8e55a48930bd
Create Date: 2017-10-05 23:20:27.369239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f09bb773fb0'
down_revision = '8e55a48930bd'
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
    sa.Column('bucketlist_id', sa.Integer(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
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
