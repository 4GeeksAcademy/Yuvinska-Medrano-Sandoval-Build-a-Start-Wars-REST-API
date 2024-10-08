"""empty message

Revision ID: 1507b5e0536f
Revises: a5cffa318ac2
Create Date: 2024-08-30 09:43:15.247654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1507b5e0536f'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('height', sa.String(length=5), nullable=False),
    sa.Column('weight', sa.String(length=5), nullable=False),
    sa.Column('hair_color', sa.String(length=15), nullable=True),
    sa.Column('skin_color', sa.String(length=15), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_character_name'), ['name'], unique=False)

    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('territory', sa.String(length=25), nullable=False),
    sa.Column('population', sa.String(length=15), nullable=False),
    sa.Column('diameter', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_planet_name'), ['name'], unique=False)

    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=18), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('username')

    op.drop_table('favorite')
    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_planet_name'))

    op.drop_table('planet')
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_character_name'))

    op.drop_table('character')
    # ### end Alembic commands ###
