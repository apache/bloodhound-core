# New Bloodhound

## Getting the Bloodhound Code:

Note that this document describes a new Apache Bloodhound project that is
intending to replace the Trac-based version. If you are interested in that
version, the appropriate code is available from [here][Legacy Repo].

The new version of Apache Bloodhound is in the bloodhound-core git repository
which is mirrored on GitHub [here][GitHub Mirror].

If you have not already got the code, you can clone the repo with the
following command:

```
git clone https://github.com/apache/bloodhound-core.git
```

which will put the code in the `bloodhound-core` directory.

[Legacy Repo]: https://svn.apache.org/repos/asf/bloodhound/
[GitHub Mirror]: https://github.com/apache/bloodhound-core

## Prerequisites

This version of Apache Bloodhound requires Python, Poetry and Django.

### Installing Python

The versions of Python that can be used are currently 3.8, 3.9 and 3.10.

Where convenient is it sensible to go for the newest release of Python that
you can.

Modern Linux and BSD distributions will have new enough Python 3 packages in
their repos and are often already installed if it is not a minimal
installation. For these cases it will usually be sensible to take advantage of
this.

If this is not the case, you can look for advice from:

 * [The Hitchhiker's Guide to Python][Python Guide] for their installation guides on
   Mac OS X, Windows and Linux.
 * The official Python documentation on [Setup and Usage][Python Usage] which
   includes information for installing on more Unix platforms, Windows and Mac.

[Python Guide]: https://docs.python-guide.org/
[Python Usage]: https://docs.python.org/3/using/

### Installing Poetry

The project now uses [Poetry][Poetry] for python environment management and
looking after further dependencies.

If you are installing on linux, it is possible that poetry is installable from
the repositories for your distro. For example, on recent Fedora releases, the
following should work:

```
sudo dnf install poetry
```

For anywhere else you can consider following the instructions from the
[Poetry documentation][Poetry Docs].

Once installed, optionally you can pre-configure poetry to make it use a
`.venv` directory at the root of poetry projects. This can be helpful as it
makes this easier to find and removal of your copy of the git repo will also
clean up these files. If this seems useful:

```
poetry config virtualenvs.in-project true
```

As Poetry creates and manages python virtual environments (virtualenv) for you,
it is useful to be aware of how they are used. For convenience, throughout this
document, any command that requires the virtualenv to be 'active' will be
provided with `poetry run` before the command. While this may get old, it is
effectively robust as it should work without having to remind you all the time
to be sure the virtualenv is activated.

For a little more completeness, the following lists the options along with
example sessions, each including a command to demonstrate exiting the
virtualenv if applicable:

 * prefix commands that require the virtualenv with `poetry run`:
   ```
   poetry run python --version
   poetry run django-admin help
   ```
 * start the `poetry shell`:
   ```
   poetry shell
   python --version
   django-admin help
   exit
   ```
 * activate the virtualenv manually (example for bash and assumes the
   suggested `virtualenvs.in-project` option was set):
   ```
   source .venv/bin/activate
   python --version
   django-admin help
   deactivate
   ```

[Poetry]: https://python-poetry.org/
[Poetry Docs]: https://python-poetry.org/docs/

## Preparing the Python environment

It should now be possible to use poetry to install the rest of the project
dependencies.

From the root of the project folder (probably `bloodhound-core` if the above
instructions have been followed) run:

```
poetry install
```

## Setup

The basic setup steps to get running are:

```
poetry run python manage.py makemigrations trackers
poetry run python manage.py migrate
```

The above will do the basic database setup.

Note that currently models are in flux and, for the moment, no support should
be expected for migrations as models change. This will change when basic
models gain stability.

## Setting up a superuser

For certain operations it will be useful to have accounts and superusers to
work with. There are a few ways to add a superuser. For interactive use, the
`createsuperuser` action is usually straightforward enough:

```
poetry run python manage.py createsuperuser --email admin@example.com --username admin
```

Entering the password twice on prompting is currently required. If the options
for `--username` and `--email` are skipped, the command will request these
details first.

## Running the development server:

```
poetry run python manage.py runserver
```

Amongst the initial output of that command will be something like:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Currently, there is not much to see at the specified location. More work has
been done on the core API. The following views may be of interest as you
explore:

 * http://127.0.0.1:8000/swagger/
 * http://127.0.0.1:8000/redoc/
 * http://127.0.0.1:8000/api/

These paths are subject to change.

## Unit Tests

Unit tests are currently being written with the standard unittest framework.
This may be replaced with pytest.

Unit tests are run with the following command:

```
poetry run python manage.py test trackers
```

## Integration Tests

The integration tests are based on [Selenium] and Firefox. For convenience of
setup, these tests currently expect to connect to Selenium at

  http://127.0.0.1:4444/wd/hub

If you have docker-compose installed, the `selenium-firefox` container can be
brought up from the `docker` directory with:

```
docker-compose up -d selenium-firefox
```

Or, with just docker (from any directory):

```
docker run -d --network host --privileged --name server \
        docker.io/selenium/standalone-firefox
```

Running the functional tests directly requires a running server and so run

```
poetry run python manage.py runserver
```

in one terminal and in a second:

```
poetry run python functional_tests.py
```

There are currently not many tests - those that are there are in place to test
the setup above and assume that there will be useful tests in due course.

[Selenium]: https://selenium.dev/

## Development notes:

Fixtures for tests when required can be generated with:

```
poetry run python manage.py dumpdata trackers --format=yaml --indent=2 > trackers/fixtures/[fixture-name].yaml
```

## Postgresql Support

While the sqlite database backend is convenient to reduce the complexity of
setting up development environments, Django provides us with options to use a
range of database backends.

Initially we will concentrate on making it easier to support the Postgresql
backend.

### Requirements for connecting to a Postgresql database

There are a number of options available to satisfy the dependencies for
Postgresql support. For convenience we provide two alternatives through our
poetry setup.

Full installation for production like installation should use the following
steps:

 1. Provide build dependencies (example for Fedora):
    ```
    sudo dnf install gcc python3-devel libpq-devel
    ```
 2. Use poetry to install the python dependencies from pypi:
    ```
    poetry install --extras=postgres
    ```

Alternatively it is possible to avoid providing the build dependencies and
instead follow the simplified steps:

 1. Use poetry to install the simplified python dependencies:
    ```
    poetry install --extras=postgres-binary
    ```

While we recommend the first option, particularly for production deployments,
the simplified option may be pragmatic for setting up for development or
testing.

### Running Postgresql

Although at this point we should have the ability to connect to a database
through python, we have not addressed actually running a Postgresql database.

For convenience, for development and testing purposes we are going to use
containers (docker/podman) to address this. Other possibilities for this exist
including installing and configuring postgresql-server but that is currently
beyond the scope of this document.

There is a docker folder at the base of the repo that, with a suitable docker
host environment can be used to start up a postgresql database container.

The docker/db/scripts directory allows for the provision of valid sql commands
in *sql files that will be copied into the container and used to initialize
the database if required.

If you have docker-compose installed, the db container can be brought up from
the `docker` directory with:

```
docker-compose up -d db
```

### Specifying the Postgresql Backend

Finally you will need to specify the database to connect to. At the moment
this can be achieved by editing the bh_core/settings.py file to change the
DATABASES to look something like this, depending on the actual connection
details.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bloodhound',
        'USER': 'bloodhound',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
     }
 }
 ```

Note that this aspect of the setup should be expected to change to smooth over
some of the difficulties around editing a file that is in source control.

## Notes on using podman instead of docker

If you have podman instead of docker, the `podman` command should work as a
drop-in replacement for `docker` commands where these are used in this README.

It should also now be possible to use `docker-compose` commands directly with
a little preparation. Consult [this article][Use docker-compose with podman]
for details but note that, at the time of writing, there is an error in the
article and you will need to use

```
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock
```

to successfully run `docker-compose` commands.

[Use docker-compose with podman]: https://fedoramagazine.org/use-docker-compose-with-podman-to-orchestrate-containers-on-fedora/
