"""v0.1.0-add-pool-stats-30d

Revision ID: 98ee638ebbf7
Revises: 29839775b6c1
Create Date: 2023-03-05 20:19:42.006040

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '98ee638ebbf7'
down_revision = '29839775b6c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pools', sa.Column('base_volume_30d', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('quote_volume_30d', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('base_lp_fees_30d', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('quote_lp_fees_30d', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('base_baln_fees_30d', sa.Float(), nullable=True))
    op.add_column('pools', sa.Column('quote_baln_fees_30d', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pools', 'quote_baln_fees_30d')
    op.drop_column('pools', 'base_baln_fees_30d')
    op.drop_column('pools', 'quote_lp_fees_30d')
    op.drop_column('pools', 'base_lp_fees_30d')
    op.drop_column('pools', 'quote_volume_30d')
    op.drop_column('pools', 'base_volume_30d')
    # ### end Alembic commands ###
