"""empty message

Revision ID: 76152dfce252
Revises: ed11eaa4895c
Create Date: 2023-12-01 10:56:29.099195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76152dfce252'
down_revision = 'ed11eaa4895c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
