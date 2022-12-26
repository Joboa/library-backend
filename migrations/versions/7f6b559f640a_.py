"""empty message

Revision ID: 7f6b559f640a
Revises: a6a567ec2a0d
Create Date: 2022-12-26 16:59:59.222365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f6b559f640a'
down_revision = 'a6a567ec2a0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('edition', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('book_type', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('journals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('title', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('publisher', sa.String(length=500), nullable=False))
        batch_op.add_column(sa.Column('publication_date', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('first_author', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('second_author', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('last_author', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('authors_shorten', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('url_to_journal', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('username', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('password', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('password')
        batch_op.drop_column('email')
        batch_op.drop_column('username')
        batch_op.drop_column('id')

    with op.batch_alter_table('journals', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('user_id')
        batch_op.drop_column('url_to_journal')
        batch_op.drop_column('authors_shorten')
        batch_op.drop_column('last_author')
        batch_op.drop_column('second_author')
        batch_op.drop_column('first_author')
        batch_op.drop_column('publication_date')
        batch_op.drop_column('publisher')
        batch_op.drop_column('title')
        batch_op.drop_column('id')

    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')
        batch_op.drop_column('user_id')
        batch_op.drop_column('book_type')
        batch_op.drop_column('edition')
        batch_op.drop_column('title')
        batch_op.drop_column('id')

    # ### end Alembic commands ###
