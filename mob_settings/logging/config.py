import logging

import logzero

DEFAULT_FORMAT = '%(color)s%(asctime)s-%(threadName)s|%(filename)s:%(lineno)d|%(levelname)-7s%(''end_color)s : %(message)s'


def syslog(name='app', level=logging.DEBUG, fmt=DEFAULT_FORMAT):
    formatter = logzero.LogFormatter(fmt=fmt)
    return logzero.setup_logger(
        name=name,
        level=level,
        formatter=formatter
    )


def filelog(name='app', file_name='app.log', level=logging.DEBUG, fmt=DEFAULT_FORMAT, max_bytes=1000, backup_count=3,
            disable_stderr=False):
    formatter = logzero.LogFormatter(fmt=fmt)
    return logzero.setup_logger(
        name=name,
        logfile=file_name,
        level=level,
        formatter=formatter,
        maxBytes=max_bytes,
        backupCount=backup_count,
        fileLoglevel=level,
        disableStderrLogger=disable_stderr
    )
