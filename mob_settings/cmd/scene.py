import click

from mob_settings.cmd import port
from mob_settings.db import proxy
from mob_settings.db.proxy import SqliteConfig
from mob_settings.logging import syslog


class SceneOption(object):

    def __init__(self, profile, database, file):
        self.profile = profile
        self.database = database
        self.file = file


@click.group("scene", invoke_without_command=True)
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

    ctx.obj = SceneOption(profile, database, file)

    if ctx.invoked_subcommand is None:
        __list(ctx)


@click.command("save")
@click.option('--values', type=(str, str), multiple=True)
@click.pass_obj
def save(scene_option, values):
    syslog().debug('scene save start')

    with proxy.connection().atomic() as tx:
        port.scene_save(values)

    syslog().debug('scene save end')


@click.command("list")
@click.pass_obj
def _list(scene_option):
    __list(scene_option)


def __list(scene_option):
    syslog().debug('scene list start')

    records = port.scene_list()
    for r in records:
        syslog().debug(f'{r.id}, {r.code}')

    syslog().debug('scene list end')


cmd.add_command(save)
cmd.add_command(_list)
