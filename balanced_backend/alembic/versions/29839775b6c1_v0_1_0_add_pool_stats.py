"""v0.1.0-add-pool-stats

Revision ID: 29839775b6c1
Revises: a51236f82a74
Create Date: 2023-03-05 19:39:57.817951

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '29839775b6c1'
down_revision = 'a51236f82a74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pools', sa.Column('base_lp_fees_24h', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('quote_lp_fees_24h', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('base_baln_fees_24h', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('quote_baln_fees_24h', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pools', 'quote_baln_fees_24h')
    op.drop_column('pools', 'base_baln_fees_24h')
    op.drop_column('pools', 'quote_lp_fees_24h')
    op.drop_column('pools', 'base_lp_fees_24h')
    # ### end Alembic commands ###
