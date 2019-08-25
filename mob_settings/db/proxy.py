from peewee import *
from playhouse.pool import PooledSqliteExtDatabase

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


def initialize(profile='dev', config=None):
    if profile == 'dev':
        database = SqliteDatabase(':memory:')
    else:
        if config.name == 'sqlite':
            database = PooledSqliteExtDatabase(config.db_file, max_connections=32, stale_timeout=600,
                                               pragmas={
                                                   'journal_mode': 'wal',
                                                   'cache_size': -1 * 64000,  # 64MB
                                                   'foreign_keys': 1,
                                                   'ignore_check_constraints': 0,
                                                   'synchronous': 0})
        else:
            raise ValueError(f'Not supported {config.name}.')

    database_proxy.initialize(database)


def connection():
    return database_proxy


class BaseDatabase(object):
    def __init__(self, name):
        self.name = name


class SqliteConfig(BaseDatabase):
    def __init__(self, db_file):
        super().__init__('sqlite')
        self.db_file = db_file
