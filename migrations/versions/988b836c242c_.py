"""empty message

Revision ID: 988b836c242c
Revises: 648b00a83984
Create Date: 2016-05-27 16:39:42.869855

"""

# revision identifiers, used by Alembic.
revision = '988b836c242c'
down_revision = '648b00a83984'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('bucket_list_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('done', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('bucketlist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bucketlist_id'], ['bucket_list.id'], ),
    sa.PrimaryKeyConstraint('id'))

def downgrade():
    pass
