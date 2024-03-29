"""v0.1.0

Revision ID: 33ca2f0bef3a
Revises: e812ecf96b8e
Create Date: 2023-02-20 00:41:13.664033

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '33ca2f0bef3a'
down_revision = 'e812ecf96b8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dex_swaps',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('transaction_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('log_index', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('block_number', sa.Integer(), nullable=True),
    sa.Column('pool_id', sa.Integer(), nullable=True),
    sa.Column('from_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('to_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('base_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('base_token_value', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('base_token_value_decimal', sa.Float(), nullable=True),
    sa.Column('quote_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('quote_token_value', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('quote_token_value_decimal', sa.Float(), nullable=True),
    sa.Column('sender', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('receiver', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('from_value', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('to_value', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('lp_fees', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('baln_fees', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('pool_base', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('pool_quote', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('ending_price', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('effective_fill_price', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('from_value_decimal', sa.Float(), nullable=True),
    sa.Column('to_value_decimal', sa.Float(), nullable=True),
    sa.Column('lp_fees_decimal', sa.Float(), nullable=True),
    sa.Column('baln_fees_decimal', sa.Float(), nullable=True),
    sa.Column('pool_base_decimal', sa.Float(), nullable=True),
    sa.Column('pool_quote_decimal', sa.Float(), nullable=True),
    sa.Column('ending_price_decimal', sa.Float(), nullable=True),
    sa.Column('effective_fill_price_decimal', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'transaction_hash', 'log_index')
    )
    op.create_index(op.f('ix_dex_swaps_block_number'), 'dex_swaps', ['block_number'], unique=False)
    op.create_index(op.f('ix_dex_swaps_timestamp'), 'dex_swaps', ['timestamp'], unique=False)
    op.create_table('pools',
    sa.Column('base_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('quote_address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('chain_id', sa.Integer(), nullable=True),
    sa.Column('pool_id', sa.Integer(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('base_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('quote_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('base_symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('quote_symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('base_decimals', sa.Integer(), nullable=True),
    sa.Column('quote_decimals', sa.Integer(), nullable=True),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('price_change_24h', sa.Float(), nullable=True),
    sa.Column('price_change_7d', sa.Float(), nullable=True),
    sa.Column('price_change_30d', sa.Float(), nullable=True),
    sa.Column('base_price', sa.Float(), nullable=True),
    sa.Column('quote_price', sa.Float(), nullable=True),
    sa.Column('base_supply', sa.Float(), nullable=True),
    sa.Column('quote_supply', sa.Float(), nullable=True),
    sa.Column('base_liquidity', sa.Float(), nullable=True),
    sa.Column('quote_liquidity', sa.Float(), nullable=True),
    sa.Column('holders', sa.Integer(), nullable=True),
    sa.Column('total_supply', sa.Float(), nullable=True),
    sa.Column('last_updated_timestamp', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('base_address', 'quote_address')
    )
    op.create_index(op.f('ix_pools_base_address'), 'pools', ['base_address'], unique=False)
    op.create_index(op.f('ix_pools_chain_id'), 'pools', ['chain_id'], unique=False)
    op.create_index(op.f('ix_pools_pool_id'), 'pools', ['pool_id'], unique=False)
    op.create_index(op.f('ix_pools_quote_address'), 'pools', ['quote_address'], unique=False)
    op.create_table('token_pool',
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('chain_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=True),
    sa.Column('pool_price', sa.Float(), nullable=True),
    sa.Column('pool_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('total_supply', sa.Float(), nullable=True),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('supply', sa.Float(), nullable=True),
    sa.Column('reference_address', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('reference_symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('reference_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('reference_price', sa.Float(), nullable=True),
    sa.Column('reference_supply', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('pool_id', 'address')
    )
    op.create_index(op.f('ix_token_pool_chain_id'), 'token_pool', ['chain_id'], unique=False)
    op.create_index(op.f('ix_token_pool_reference_address'), 'token_pool', ['reference_address'], unique=False)
    op.create_index(op.f('ix_token_pool_reference_symbol'), 'token_pool', ['reference_symbol'], unique=False)
    op.create_index(op.f('ix_token_pool_symbol'), 'token_pool', ['symbol'], unique=False)
    op.create_table('token_prices',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('chain_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('total_supply', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('name', 'timestamp')
    )
    op.create_index(op.f('ix_token_prices_chain_id'), 'token_prices', ['chain_id'], unique=False)
    op.create_table('tokens',
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('symbol', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('decimals', sa.Integer(), nullable=True),
    sa.Column('logo_uri', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('price_24h', sa.Float(), nullable=True),
    sa.Column('price_7d', sa.Float(), nullable=True),
    sa.Column('price_30d', sa.Float(), nullable=True),
    sa.Column('holders', sa.Integer(), nullable=True),
    sa.Column('total_supply', sa.Float(), nullable=True),
    sa.Column('volume', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('volume_decimal', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('lp_fees', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('lp_fees_decimal', sa.Float(), nullable=True),
    sa.Column('baln_fees', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('baln_fees_decimal', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('address', 'chain_id')
    )
    op.create_index(op.f('ix_tokens_address'), 'tokens', ['address'], unique=False)
    op.create_index(op.f('ix_tokens_chain_id'), 'tokens', ['chain_id'], unique=False)
    op.create_table('volume_series_15_min',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('base_volume', sa.Float(), nullable=True),
    sa.Column('quote_volume', sa.Float(), nullable=True),
    sa.Column('lp_fees', sa.Float(), nullable=True),
    sa.Column('baln_fees', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id', 'timestamp')
    )
    op.create_table('volume_series_1_day',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('base_volume', sa.Float(), nullable=True),
    sa.Column('quote_volume', sa.Float(), nullable=True),
    sa.Column('lp_fees', sa.Float(), nullable=True),
    sa.Column('baln_fees', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id', 'timestamp')
    )
    op.create_table('volume_series_1_hour',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('base_volume', sa.Float(), nullable=True),
    sa.Column('quote_volume', sa.Float(), nullable=True),
    sa.Column('lp_fees', sa.Float(), nullable=True),
    sa.Column('baln_fees', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id', 'timestamp')
    )
    op.create_table('volume_series_1_month',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('base_volume', sa.Float(), nullable=True),
    sa.Column('quote_volume', sa.Float(), nullable=True),
    sa.Column('lp_fees', sa.Float(), nullable=True),
    sa.Column('baln_fees', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id', 'timestamp')
    )
    op.create_table('volume_series_1_week',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('base_volume', sa.Float(), nullable=True),
    sa.Column('quote_volume', sa.Float(), nullable=True),
    sa.Column('lp_fees', sa.Float(), nullable=True),
    sa.Column('baln_fees', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id', 'timestamp')
    )
    op.create_table('volume_series_4_hour',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('base_volume', sa.Float(), nullable=True),
    sa.Column('quote_volume', sa.Float(), nullable=True),
    sa.Column('lp_fees', sa.Float(), nullable=True),
    sa.Column('baln_fees', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id', 'timestamp')
    )
    op.create_table('volume_series_5_min',
    sa.Column('chain_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.Integer(), nullable=False),
    sa.Column('close', sa.Float(), nullable=True),
    sa.Column('open', sa.Float(), nullable=True),
    sa.Column('high', sa.Float(), nullable=True),
    sa.Column('low', sa.Float(), nullable=True),
    sa.Column('base_volume', sa.Float(), nullable=True),
    sa.Column('quote_volume', sa.Float(), nullable=True),
    sa.Column('lp_fees', sa.Float(), nullable=True),
    sa.Column('baln_fees', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('chain_id', 'pool_id', 'timestamp')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('volume_series_5_min')
    op.drop_table('volume_series_4_hour')
    op.drop_table('volume_series_1_week')
    op.drop_table('volume_series_1_month')
    op.drop_table('volume_series_1_hour')
    op.drop_table('volume_series_1_day')
    op.drop_table('volume_series_15_min')
    op.drop_index(op.f('ix_tokens_chain_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_address'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_token_prices_chain_id'), table_name='token_prices')
    op.drop_table('token_prices')
    op.drop_index(op.f('ix_token_pool_symbol'), table_name='token_pool')
    op.drop_index(op.f('ix_token_pool_reference_symbol'), table_name='token_pool')
    op.drop_index(op.f('ix_token_pool_reference_address'), table_name='token_pool')
    op.drop_index(op.f('ix_token_pool_chain_id'), table_name='token_pool')
    op.drop_table('token_pool')
    op.drop_index(op.f('ix_pools_quote_address'), table_name='pools')
    op.drop_index(op.f('ix_pools_pool_id'), table_name='pools')
    op.drop_index(op.f('ix_pools_chain_id'), table_name='pools')
    op.drop_index(op.f('ix_pools_base_address'), table_name='pools')
    op.drop_table('pools')
    op.drop_index(op.f('ix_dex_swaps_timestamp'), table_name='dex_swaps')
    op.drop_index(op.f('ix_dex_swaps_block_number'), table_name='dex_swaps')
    op.drop_table('dex_swaps')
    # ### end Alembic commands ###
