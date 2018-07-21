"""
    Helpers for different functions
"""
import logging

class ColoredFormatter(logging.Formatter):
    """
        Class to create a log output which is colored based on level.
    """
    def __init__(self, *args, **kwargs):
        super(ColoredFormatter, self).__init__(*args, **kwargs)
        self.colors = {
                'DEBUG' : '\033[94m',
                'INFO'  : '\033[92m',
                'WARNING' : '\033[93m',
                'ERROR' : '\033[91m',
        }

        self.reset = '\033[0m'

    def format(self, record):
        msg = str(record.msg)
        level_name = str(record.levelname)
        name = str(record.name)
        color_prefix = self.colors[level_name]
        return '{0}{1:<9s} - {2:<25s} : {3}{4}'.format(
                color_prefix,
                '[' + level_name + ']',
                name,
                msg,
                self.reset)
