=============================
where-to-go
=============================

This is a learning project build for dvmn.
The goal of the project is to build a backend for website,
that lets you tag different places on a map.
This project uses premade `frontend`_.

This project is build with `test-django-template`_ - template  used for
experiments with project setup to get a better grasp on django projects
structure and development processes.

You can check out deployed version here: `where-to-go-moscow.herokuapp.com`_.
Change your browser preferred language to see Eng or Ru version.

If you want to add some locations - use admin interface.
`Contact me`_ to get its address and also username and a password for it.
When you log in go to ``Places -> add`` or ``Места -> Добавить``, depending
on locale you use. It should be pretty straightforward from there.
Note when editing Place you can change images order by dragging them.

This project loads places dynamically, so even there's a LOT of places in
you database, only small part of them will be loaded (as for now it's part
of the map you view extended by x1.5 factor for each side). Note however
that fronted will still be laggy if there's too much places onscreen (TODO optimize frontend).

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

.. _create superuser:

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

Creating test data
==================

There's two ways to create a test data:

1. You can `create superuser`_ and then add places and images
with admin interface.

2. Load a place from json with a management command:

.. code-block:: shell

   python manage.py load_place http://path/to.json

You can find json files with `example places here`_.
Use ``raw`` file address as a path to load it.

Those are example commands, adjust them whether you use docker or
local development environment.


Management commands
===================

There's a custom management command ``wait_for_db`` in user app.
As name suggests, it can be used to wait for postgres db to become
available, ``docker-compose.yml`` contain commented out code,
showing how to use that command instead of current implementation
with ``entrypoint`` file (borrowed from `django-cookiecutter`_).

There's also project specific ``load place`` command, described above.


Compiling translations
======================

If you want for this site to be available in multiple languages
you have to complile message files (currently there's only Russian translation).

.. code-block::shell

   python manage.py compilemessages --settings=server.settings.local

If you want to create your own translation refer to `django translation docs`_.


TODOs
=====

* Add CMS instead of managing content with admin interface
* Serve frontend separately, setup CORS
* Load data only for displayed portion of the map (use PostGIS prolly?)

Maybe
^^^^^
* Add different roles (user, moderator)
* Add commenting system
* Setup docker production deploy to ECS


.. _Docker: https://docs.docker.com/get-docker/
.. _docker-compose: https://docs.docker.com/compose/install/
.. _docker postgres options: https://hub.docker.com/_/postgres/
.. _this article: https://www.digitalocean.com/community/tutorials/common-python-tools-using-virtualenv-installing-with-pip-and-managing-packages#a-thorough-virtualenv-how-to
.. _django-extensions: https://github.com/django-extensions/django-extensions
.. _localhost: http://localhost:8000/
.. _test-django-template: https://github.com/aleert/test-django-template
.. _django-cookiecutter: https://github.com/pydanny/cookiecutter-django
.. _frontend: https://github.com/devmanorg/where-to-go-frontend/
.. _example places here: https://github.com/devmanorg/where-to-go-places/tree/master/places
.. _django translation docs: https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#localization-how-to-create-language-files
.. _where-to-go-moscow.herokuapp.com: https://where-to-go-moscow.herokuapp.com
.. _Contact me: mailto:aleert@yandex.ru
