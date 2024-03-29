"""v0.1.0-add-dividends

Revision ID: 80f136ddaec4
Revises: 33ca2f0bef3a
Create Date: 2023-02-22 15:34:21.249917

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '80f136ddaec4'
down_revision = '33ca2f0bef3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dividends',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('base_address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('quote_address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('base_lp_fees_24h', sa.Float(), nullable=True),
    sa.Column('quote_lp_fees_24h', sa.Float(), nullable=True),
    sa.Column('base_baln_fees_24h', sa.Float(), nullable=True),
    sa.Column('quote_baln_fees_24h', sa.Float(), nullable=True),
    sa.Column('base_volume_24h', sa.Float(), nullable=True),
    sa.Column('quote_volume_24h', sa.Float(), nullable=True),
    sa.Column('base_lp_fees_30d', sa.Float(), nullable=True),
    sa.Column('quote_lp_fees_30d', sa.Float(), nullable=True),
    sa.Column('base_baln_fees_30d', sa.Float(), nullable=True),
    sa.Column('quote_baln_fees_30d', sa.Float(), nullable=True),
    sa.Column('base_volume_30d', sa.Float(), nullable=True),
    sa.Column('quote_volume_30d', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id')
    )
    op.create_index(op.f('ix_dividends_base_address'), 'dividends', ['base_address'], unique=False)
    op.create_index(op.f('ix_dividends_quote_address'), 'dividends', ['quote_address'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dividends_quote_address'), table_name='dividends')
    op.drop_index(op.f('ix_dividends_base_address'), table_name='dividends')
    op.drop_table('dividends')
    # ### end Alembic commands ###
