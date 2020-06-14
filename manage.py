#!/usr/bin/env python

import sys

from django.core.management.base import OutputWrapper, color_style

style = color_style()
stdout = OutputWrapper(out=sys.stdout)


def main():
    """
    Main function.

    It does several things:
    1. Sets default settings module, if it is not set
    2. Warns if Django is not installed
    3. Executes any given command
    4. Issues warning if you're using local environment.
    """
    try:
        from django.core import management  # noqa: WPS433
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and " +
                'available on your PYTHONPATH environment variable? Did you ' +
                'forget to activate a virtual environment?',
            )
        raise

    management.execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
