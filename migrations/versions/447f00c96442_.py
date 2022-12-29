"""empty message

Revision ID: 447f00c96442
Revises: 1dffc4008ecb
Create Date: 2022-12-27 13:49:10.955164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '447f00c96442'
down_revision = '1dffc4008ecb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_user', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('edition', sa.String(length=255), nullable=True),
    sa.Column('book_type', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('journals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('publisher', sa.String(length=500), nullable=False),
    sa.Column('publication_date', sa.String(length=100), nullable=True),
    sa.Column('first_author', sa.String(length=255), nullable=False),
    sa.Column('second_author', sa.String(length=255), nullable=True),
    sa.Column('last_author', sa.String(length=255), nullable=True),
    sa.Column('authors_shorten', sa.Text(), nullable=True),
    sa.Column('url_to_journal', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('journals')
    op.drop_table('books')
    op.drop_table('users')
    # ### end Alembic commands ###
