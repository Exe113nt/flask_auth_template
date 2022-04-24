"""product owner

Revision ID: 7c69c17b9088
Revises: 28ed2b7cb97a
Create Date: 2022-04-24 13:14:16.317359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c69c17b9088'
down_revision = '28ed2b7cb97a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'product', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_column('product', 'owner_id')
    # ### end Alembic commands ###
