import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mob_settings.cmd.root import cmd


def main():
    cmd()


if __name__ == '__main__':
    main()
