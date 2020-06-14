=============================
where-to-go
=============================

This is a learning project build for dvmn.
The goal of the project is to build a backend for website,
that lets you tag different places on a map.

This project is build with `test-django-template`_ - template  used for
experiments with project setup to get a better grasp on django projects
structure and development processes.

Running with docker
===================

Requirements
^^^^^^^^^^^^

To run this project with docker you'll need `Docker`_ installed
as well as `docker-compose`_.

Setting up environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First you need to create ``.envs/.django/.django``
and ``.envs/.postgres/.postgres`` environmental files.

Run

.. code-block:: shell

   ./generate_env.sh

to generate them automatically. Note that will not set API keys for you.

See `docker postgres options`_ to learn more about postgres environment variables,
specific for docker setup.

.. _building docker images:

Building docker images
^^^^^^^^^^^^^^^^^^^^^^

Run

.. code-block:: shell

   docker-compose build

to build required images.

Running a project
^^^^^^^^^^^^^^^^^

To run a project use:

.. code-block:: shell

   docker-compose up

then go to `localhost`_ to see it live.

Use

.. code-block:: shell

   docker-compose down

in separate shell to stop and remove containers.
Alternatively press ``Ctrl-C`` in shell where docker-compose is running
and then use ``docker-compose down``.

Running specific commands
^^^^^^^^^^^^^^^^^^^^^^^^^

To run specific command within a container do this:

.. code-block:: shell

   docker-compose run --rm <container-name> <command>

Creating a superuser
~~~~~~~~~~~~~~~~~~~~

For example, to create a superuser run

.. code-block:: shell

   docker-compose run --rm django python manage.py createsuperuser --noinput

That will create superuser with username and password specified
if ``.envs/.local/.django/.django``. Default ones are ``admin`` and ``admin_password``.

Entering django shell
~~~~~~~~~~~~~~~~~~~~~

This project has `django-extensions`_ installed, so you can use
``shell_plus`` instead of regular django shell:

.. code-block:: shell

   docker-compose run --rm django python manage.py shell_plus

Running test suite
~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   docker-compose run --rm django pytest

For linting run

.. code-block:: shell

   docker-compose run --rm django flake8

Rebuilding docker images after changing environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you changed environment variables related to postgres database (username, password etc.)
you'll have to clean postgres image volumes before rebuilding db image,
otherwise database with new parameters will not be initialized.

First, stop running containers:

.. code-block:: shell

   docker-compose down

Then remove postgres container volumes:

.. code-block:: shell

   docker volume rm where-to-go_postgres_backup_dev where-to-go_postgres_data_dev

Alternatively you can remove all volumes by

.. code-block:: shell

   docker volume rm $(docker volume ls -q)

After that you can build image as described in `building docker images`_ section.

You can pass ``--no-cache`` option to rebuild images
without using cached layers. To rebuild specific image
specify it's name after ``docker-compose build``


Running locally
===============

Requirements
^^^^^^^^^^^^

To run locally you'll need:

1. python3.8+
2. postgresql 11+

Preparing development environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's suggested you run this project in a separate python virtual environment.
To learn how to set up one read `this article`_.


Installing project requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you activated your virtual environment run

.. code-block:: shell

   pip install -r requirements/local.txt

Setting up environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run project with docker you need to create ``.envs/.django/.env``
and ``.envs/.postgres/.postgres`` environmental files.

Run

.. code-block:: shell

   ./generate_env.sh

to generate them automatically. Note that will not set API keys for you.

Creating database
^^^^^^^^^^^^^^^^^

``generate_env.sh`` also created an ``initdb.sh`` script to help you
with database management.
You can run

.. code-block:: shell

   ./initdb.sh create

to create a database or

.. code-block:: shell

   ./initdb.sh drop

to delete it.

Running mirgations
^^^^^^^^^^^^^^^^^^

Run

.. code-block:: shell

   python manage.py migrate --settings=server.settings.local

to apply migrations.

Note that we do not have default settings module so you should
point to one explicitly with ``--setting`` flag or specify one in
and environment variable: ``export DJANGO_SETTINGS_MODULE=server.settings.local``.

Starting a project
^^^^^^^^^^^^^^^^^^

After applying migrations run

.. code-block:: shell

   python manage.py server_plus --settings=server.settings.local

to run a project.

Go to `localhost`_ to see it live.

Management commands
===================

There's a custom management command ``wait_for_db`` in user app.
As name suggests, it can be used to wait for postgres db to become
available, ``docker-compose.yml`` contain commented out code,
showing how to use that command instead of current implementation
with ``entrypoint`` file (borrowed from `django-cookiecutter`_).


.. _Docker: https://docs.docker.com/get-docker/
.. _docker-compose: https://docs.docker.com/compose/install/
.. _docker postgres options: https://hub.docker.com/_/postgres/
.. _this article: https://www.digitalocean.com/community/tutorials/common-python-tools-using-virtualenv-installing-with-pip-and-managing-packages#a-thorough-virtualenv-how-to
.. _django-extensions: https://github.com/django-extensions/django-extensions
.. _localhost: http://localhost:8000/
.. _test-django-template: https://github.com/aleert/test-django-template
.. _django-cookiecutter: https://github.com/pydanny/cookiecutter-django
