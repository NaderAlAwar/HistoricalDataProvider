"""changed schema

Revision ID: 443be0eb93f
Revises: 
Create Date: 2019-03-24 12:41:19.732288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '443be0eb93f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_daily_price',
    sa.Column('stock_ticker', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('stock_ticker', 'date')
    )
    op.create_index(op.f('ix_stock_daily_price_open_price'), 'stock_daily_price', ['open_price'], unique=False)
    op.create_table('stock_ticker_info',
    sa.Column('stock_ticker', sa.String(), nullable=False),
    sa.Column('last_accessed', sa.DateTime(), nullable=True),
    sa.Column('data_present', sa.Boolean(), nullable=True),
    sa.Column('oldest_date', sa.DateTime(), nullable=True),
    sa.Column('newest_date', sa.DateTime(), nullable=True),
    sa.Column('number_of_entries', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('stock_ticker')
    )
    op.create_index(op.f('ix_stock_ticker_info_data_present'), 'stock_ticker_info', ['data_present'], unique=False)
    op.create_index(op.f('ix_stock_ticker_info_last_accessed'), 'stock_ticker_info', ['last_accessed'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_stock_ticker_info_last_accessed'), table_name='stock_ticker_info')
    op.drop_index(op.f('ix_stock_ticker_info_data_present'), table_name='stock_ticker_info')
    op.drop_table('stock_ticker_info')
    op.drop_index(op.f('ix_stock_daily_price_open_price'), table_name='stock_daily_price')
    op.drop_table('stock_daily_price')
    ### end Alembic commands ###
