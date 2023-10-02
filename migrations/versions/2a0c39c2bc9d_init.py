"""'Init'

Revision ID: 2a0c39c2bc9d
Revises: 
Create Date: 2023-09-25 17:53:12.733355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a0c39c2bc9d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('country_ukr', sa.String(length=255), nullable=False),
    sa.Column('country_eng', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('country_id')
    )
    op.create_table('currencies',
    sa.Column('currency_id', sa.Integer(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('currency_id')
    )
    op.create_index(op.f('ix_currencies_currency_id'), 'currencies', ['currency_id'], unique=False)
    op.create_table('services',
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('service_ua', sa.String(), nullable=True),
    sa.Column('service_en', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('service_id')
    )
    op.create_index(op.f('ix_services_service_id'), 'services', ['service_id'], unique=False)
    op.create_table('subscribe_plans',
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('subscribe_plan', sa.String(), nullable=False),
    sa.Column('plan_period', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('plan_id')
    )
    op.create_index(op.f('ix_subscribe_plans_plan_id'), 'subscribe_plans', ['plan_id'], unique=False)
    op.create_table('cities',
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('city_ukr', sa.String(length=255), nullable=False),
    sa.Column('city_eng', sa.String(length=255), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.country_id'], ),
    sa.PrimaryKeyConstraint('city_id')
    )
    op.create_table('service_categories',
    sa.Column('service_category_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('service_category_ua', sa.String(), nullable=True),
    sa.Column('service_category_en', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['service_id'], ['services.service_id'], ),
    sa.PrimaryKeyConstraint('service_category_id')
    )
    op.create_index(op.f('ix_service_categories_service_category_id'), 'service_categories', ['service_category_id'], unique=False)
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('client', 'master', 'admin', 'moderator', 'superadmin', name='role'), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('banned', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], ),
    sa.ForeignKeyConstraint(['country_id'], ['countries.country_id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('last_visit', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_index(op.f('ix_admin_admin_id'), 'admin', ['admin_id'], unique=False)
    op.create_table('master_info',
    sa.Column('master_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('salon_name', sa.String(), nullable=True),
    sa.Column('salon_address', sa.String(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=True),
    sa.Column('free_period', sa.Integer(), nullable=True),
    sa.Column('plan_period', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['plan_id'], ['subscribe_plans.plan_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('master_id')
    )
    op.create_index(op.f('ix_master_info_user_id'), 'master_info', ['user_id'], unique=False)
    op.create_table('masters_m2m_services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('master_id', sa.Integer(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('service_category_id', sa.Integer(), nullable=False),
    sa.Column('service_description', sa.String(), nullable=True),
    sa.Column('service_price', sa.Float(), nullable=False),
    sa.Column('service_sale_price', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.currency_id'], ),
    sa.ForeignKeyConstraint(['master_id'], ['master_info.master_id'], ),
    sa.ForeignKeyConstraint(['service_category_id'], ['service_categories.service_category_id'], ),
    sa.ForeignKeyConstraint(['service_id'], ['services.service_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('master_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['master_id'], ['master_info.master_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_responses_id'), 'user_responses', ['id'], unique=False)
    op.create_index(op.f('ix_user_responses_user_id'), 'user_responses', ['user_id'], unique=False)
    op.create_table('work_photos',
    sa.Column('work_photo_id', sa.Integer(), nullable=False),
    sa.Column('master_id', sa.Integer(), nullable=False),
    sa.Column('work_photo_url', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['master_id'], ['master_info.master_id'], ),
    sa.PrimaryKeyConstraint('work_photo_id')
    )
    op.create_index(op.f('ix_work_photos_work_photo_id'), 'work_photos', ['work_photo_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_work_photos_work_photo_id'), table_name='work_photos')
    op.drop_table('work_photos')
    op.drop_index(op.f('ix_user_responses_user_id'), table_name='user_responses')
    op.drop_index(op.f('ix_user_responses_id'), table_name='user_responses')
    op.drop_table('user_responses')
    op.drop_table('masters_m2m_services')
    op.drop_index(op.f('ix_master_info_user_id'), table_name='master_info')
    op.drop_table('master_info')
    op.drop_index(op.f('ix_admin_admin_id'), table_name='admin')
    op.drop_table('admin')
    op.drop_table('users')
    op.drop_index(op.f('ix_service_categories_service_category_id'), table_name='service_categories')
    op.drop_table('service_categories')
    op.drop_table('cities')
    op.drop_index(op.f('ix_subscribe_plans_plan_id'), table_name='subscribe_plans')
    op.drop_table('subscribe_plans')
    op.drop_index(op.f('ix_services_service_id'), table_name='services')
    op.drop_table('services')
    op.drop_index(op.f('ix_currencies_currency_id'), table_name='currencies')
    op.drop_table('currencies')
    op.drop_table('countries')
    # ### end Alembic commands ###