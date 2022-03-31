"""add weapon

Revision ID: e01a6ada5292
Revises: ac9bb6ea5480
Create Date: 2022-03-30 11:35:32.690551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e01a6ada5292'
down_revision = 'ac9bb6ea5480'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weapon_main_stat_ascension_values',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ascension', sa.SmallInteger(), nullable=False),
    sa.Column('rarity', sa.SmallInteger(), nullable=False),
    sa.Column('ascension_value', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_main_stat_level_multipliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rarity', sa.SmallInteger(), nullable=False),
    sa.Column('tier', sa.SmallInteger(), nullable=False),
    sa.Column('level', sa.SmallInteger(), nullable=False),
    sa.Column('multiplier', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_main_stat_tiers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rarity', sa.SmallInteger(), nullable=False),
    sa.Column('start_value', sa.Float(), nullable=False),
    sa.Column('tier', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_passive_ability_cores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description_template', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_sub_stat_cores',
    sa.Column('stat', sa.String(length=10), nullable=False),
    sa.Column('start_value', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_sub_stat_level_multipliers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.SmallInteger(), nullable=False),
    sa.Column('multiplier', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_cores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('rarity', sa.SmallInteger(), nullable=False),
    sa.Column('main_stat_start_value', sa.Float(), nullable=False),
    sa.Column('sub_stat_core', sa.Integer(), nullable=False),
    sa.Column('weapon_type', sa.String(length=2), nullable=False),
    sa.Column('first_ascension_image', sa.String(length=255), nullable=False),
    sa.Column('second_ascension_image', sa.String(length=255), nullable=True),
    sa.Column('passive_ability_core', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['passive_ability_core'], ['weapon_passive_ability_cores.id'], name='fk_weapon_cores_weapon_passive_ability_cores_id_passive_ability_core'),
    sa.ForeignKeyConstraint(['sub_stat_core'], ['weapon_sub_stat_cores.id'], name='fk_weapon_cores_weapon_sub_stat_cores_id_sub_stat_core'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('passive_ability_core'),
    sa.UniqueConstraint('sub_stat_core')
    )
    op.create_table('weapon_passive_abilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('core', sa.Integer(), nullable=False),
    sa.Column('refinement', sa.SmallInteger(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['core'], ['weapon_passive_ability_cores.id'], name='fk_weapon_passive_abilities_weapon_passive_ability_cores_id_core'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_passive_ability_stat_cores',
    sa.Column('stat', sa.String(length=10), nullable=False),
    sa.Column('start_value', sa.Float(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('passive_ability_core', sa.Integer(), nullable=False),
    sa.Column('stat_type', sa.String(length=5), nullable=False),
    sa.Column('max_value', sa.Float(), nullable=False),
    sa.Column('refinement_scale', sa.Float(), nullable=False),
    sa.Column('position', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['passive_ability_core'], ['weapon_passive_ability_cores.id'], name='fk_weapon_passive_ability_stat_cores_weapon_passive_ability_cores_id_passive_ability_core'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_sub_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('core', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['core'], ['weapon_sub_stat_cores.id'], name='fk_weapon_sub_stats_weapon_sub_stat_cores_id_core'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapon_passive_ability_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('core', sa.Integer(), nullable=False),
    sa.Column('refinement', sa.SmallInteger(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['core'], ['weapon_passive_ability_stat_cores.id'], name='fk_weapon_passive_ability_stats_weapon_passive_ability_stat_cores_id_core'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('weapons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('core', sa.Integer(), nullable=False),
    sa.Column('level', sa.SmallInteger(), nullable=False),
    sa.Column('ascension', sa.SmallInteger(), nullable=False),
    sa.Column('main_stat_value', sa.Float(), nullable=False),
    sa.Column('sub_stat', sa.Integer(), nullable=False),
    sa.Column('refinement', sa.SmallInteger(), nullable=False),
    sa.Column('passive_ability', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['core'], ['weapon_cores.id'], name='fk_weapons_weapon_cores_id_core'),
    sa.ForeignKeyConstraint(['passive_ability'], ['weapon_passive_abilities.id'], name='fk_weapons_weapon_passive_abilities_id_passive_ability'),
    sa.ForeignKeyConstraint(['sub_stat'], ['weapon_sub_stats.id'], name='fk_weapons_weapon_sub_stats_id_sub_stat'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weapons')
    op.drop_table('weapon_passive_ability_stats')
    op.drop_table('weapon_sub_stats')
    op.drop_table('weapon_passive_ability_stat_cores')
    op.drop_table('weapon_passive_abilities')
    op.drop_table('weapon_cores')
    op.drop_table('weapon_sub_stat_level_multipliers')
    op.drop_table('weapon_sub_stat_cores')
    op.drop_table('weapon_passive_ability_cores')
    op.drop_table('weapon_main_stat_tiers')
    op.drop_table('weapon_main_stat_level_multipliers')
    op.drop_table('weapon_main_stat_ascension_values')
    # ### end Alembic commands ###