"""empty message

Revision ID: 566d50e00dd5
Revises: 12354c7317e8
Create Date: 2018-10-30 10:05:07.649353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566d50e00dd5'
down_revision = '12354c7317e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
