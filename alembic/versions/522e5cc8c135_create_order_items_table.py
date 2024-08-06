"""create order items table

Revision ID: 522e5cc8c135
Revises: cf8ed01cb0dd
Create Date: 2024-08-06 19:41:20.436463

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '522e5cc8c135'
down_revision: Union[str, None] = 'cf8ed01cb0dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('OrderItems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price_per_item', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['Orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('Orders', 'product_id')
    op.drop_column('Orders', 'is_deleted')
    op.drop_column('Orders', 'quantity')
    op.drop_column('Orders', 'updated_at')
    op.drop_column('Orders', 'price_per_item')
    op.drop_column('Orders', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Orders', sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('Orders', sa.Column('price_per_item', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('Orders', sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('Orders', sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Orders', sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('Orders', sa.Column('product_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_table('OrderItems')
    # ### end Alembic commands ###
