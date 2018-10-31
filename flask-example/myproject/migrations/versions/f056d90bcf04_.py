"""empty message

Revision ID: f056d90bcf04
Revises: fdb0d2970fdd
Create Date: 2018-10-31 16:09:31.809611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f056d90bcf04'
down_revision = 'fdb0d2970fdd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    op.drop_column('users', 'last_been')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_been', sa.DATETIME(), nullable=True))
    op.drop_column('users', 'last_seen')
    # ### end Alembic commands ###
