"""add relationship with skill

Revision ID: 2433d779a411
Revises: e3ddfb8988a7
Create Date: 2021-05-02 01:58:51.283982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2433d779a411'
down_revision = 'e3ddfb8988a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card_and_skill',
    sa.Column('card_uuid', sa.Integer(), nullable=True),
    sa.Column('skill_uuid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['card_uuid'], ['support_card.uuid'], ),
    sa.ForeignKeyConstraint(['skill_uuid'], ['skill.uuid'], )
    )
    op.create_table('uma_and_skill',
    sa.Column('uma_uuid', sa.Integer(), nullable=True),
    sa.Column('skill_uuid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['skill_uuid'], ['skill.uuid'], ),
    sa.ForeignKeyConstraint(['uma_uuid'], ['umamusume.uuid'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('uma_and_skill')
    op.drop_table('card_and_skill')
    # ### end Alembic commands ###
