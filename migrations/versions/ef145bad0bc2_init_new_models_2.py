"""Init-new-models-2

Revision ID: ef145bad0bc2
Revises: a65230ab32a3
Create Date: 2023-10-03 14:26:14.453116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef145bad0bc2'
down_revision: Union[str, None] = 'a65230ab32a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('masters_to_services', sa.Column('discount', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('masters_to_services', 'discount')
    # ### end Alembic commands ###