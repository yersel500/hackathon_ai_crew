"""change type

Revision ID: 1005ccac61ba
Revises: 4d22c0e6114a
Create Date: 2024-11-01 19:30:33.028876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1005ccac61ba'
down_revision = '4d22c0e6114a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.alter_column('processed_content_hash',
               existing_type=sa.VARCHAR(length=512),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('documents', schema=None) as batch_op:
        batch_op.alter_column('processed_content_hash',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=512),
               existing_nullable=True)

    # ### end Alembic commands ###