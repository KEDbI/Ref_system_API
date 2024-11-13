"""fix column

Revision ID: 0f0c4f11ea26
Revises: 785ab395c24c
Create Date: 2024-11-13 10:38:01.087526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f0c4f11ea26'
down_revision: Union[str, None] = '785ab395c24c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
