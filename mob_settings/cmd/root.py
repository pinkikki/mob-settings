import click

from mob_settings.cmd import scene, mob


@click.group()
def cmd():
    pass


cmd.add_command(scene.cmd)
cmd.add_command(mob.cmd)
