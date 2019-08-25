import random

import click
import yaml

from mob_settings.cmd import port
from mob_settings.db import proxy
from mob_settings.db.proxy import SqliteConfig
from mob_settings.logging import syslog


class MobOption(object):

    def __init__(self, profile, database, file):
        self.profile = profile
        self.database = database
        self.file = file


@click.group("mob", invoke_without_command=True)
@click.option('-p', '--profile', default='dev', required=True, type=click.Choice(['dev', 'prod']))
@click.option('-d', '--database', default='sqlite', required=True, type=click.Choice(['sqlite']))
@click.option('-f', '--file', type=str, envvar='MOB_SETTINGS_DATABASE_FILE')
@click.pass_context
def cmd(ctx, profile, database, file):
    syslog().debug(
        f"profile=[{profile}]. database=[{database}]. file=[{file}]")

    if database == 'sqlite':
        proxy.initialize(profile, SqliteConfig(file))
    else:
        raise click.BadParameter(
            f'Not supported database. database={database}')

    if ctx.invoked_subcommand is None:
        __list()


@click.command("save")
@click.option('-s', '--scene', type=str, default='Home')
@click.option('-ss', '--section', type=int, default=1)
@click.option('-r', '--range', '_range', type=(float, float, float, float), default=(-10, 10, -10, 10))
@click.option('-c', '--config', type=click.File('r'), required=True)
def save(scene, section, _range, config):
    syslog().debug('mob save start')
    syslog().debug(
        f"scene=[{scene}]. range=[{_range}]. config=[{config}]")

    with proxy.connection().atomic() as tx:
        with config as fc:
            c = yaml.safe_load(fc)
            mobs = c['mob']['names']
            positions = []
            scene_game_objects = []
            count = 0
            for mob in mobs:
                count += 1
                x = random.uniform(_range[0], _range[1])
                y = random.uniform(_range[2], _range[3])
                direction = random.randint(0, 3)
                positions.append(port.Position(x, y, 0.0))
                scene_game_objects.append(
                    port.SceneGameObject(scene_code=scene, scene_section=section, game_object_name=mob,
                                         scene_point=count, direction=direction))

            port.scene_point_save(scene, positions)
            port.scene_game_object_save(scene_game_objects)

    syslog().debug('mob save end')


@click.command("list")
def _list():
    __list()


def __list():
    syslog().debug('mob list start')

    records = port.scene_game_object_list()
    for r in records:
        syslog().debug(
            f'{r.id}, {r.scene_code}, {r.scene_section}, {r.game_object_name}, {r.scene_point}, {r.direction}')

    syslog().debug('mob list end')


cmd.add_command(save)
cmd.add_command(_list)
