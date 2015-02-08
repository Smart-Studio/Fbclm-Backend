#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # TODO This is a workaround to use pymsysql instead of MySQL-Python
    try:
        import pymysql

        pymysql.install_as_MySQLdb()
    except ImportError:
        pass

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fbclm.settings.settings_dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
