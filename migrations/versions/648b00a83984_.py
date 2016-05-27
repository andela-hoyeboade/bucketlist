"""empty message

Revision ID: 648b00a83984
Revises: a20149dc4aab
Create Date: 2016-05-27 16:27:32.153932

"""

# revision identifiers, used by Alembic.
revision = '648b00a83984'
down_revision = 'a20149dc4aab'

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
    sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    pass
