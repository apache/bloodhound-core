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

The versions of Python that can be used are currently 3.6, 3.7, 3.8 and 3.9.

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
poetry run python manage.py test
```

## Integration Tests

The [Selenium] tests currently require that Firefox is installed and
[geckodriver] is also on the path. If you do not already have geckodriver,
the following shows one method to get it for linux:

```
PLATFORM_EXT="linux64.tar.gz"
BIN_LOCATION="$HOME/.local/bin"
TMP_DIR=/tmp/geckodriver_download
mkdir -p "$BIN_LOCATION" "$TMP_DIR"

LATEST=$(wget -O - https://github.com/mozilla/geckodriver/releases/latest 2>&1 | awk 'match($0, /geckodriver-(v.*)-'"$PLATFORM_EXT"'/, a) {print a[1]; exit}')
wget -N -P "$TMP_DIR" "https://github.com/mozilla/geckodriver/releases/download/$LATEST/geckodriver-$LATEST-$PLATFORM_EXT"
tar -x geckodriver -zf "$TMP_DIR/geckodriver-$LATEST-$PLATFORM_EXT" -O > "$BIN_LOCATION"/geckodriver
chmod +x "$BIN_LOCATION"/geckodriver
```

If `$BIN_LOCATION` is on the system path, and the development server is
running, it should be possible to run the integration tests.

```
poetry run python functional_tests.py
```

There are currently not many tests - those that are there are in place to test
the setup above and assume that there will be useful tests in due course.

[Selenium]: https://selenium.dev/
[geckodriver]: https://firefox-source-docs.mozilla.org/testing/geckodriver/

## Development notes:

Fixtures for tests when required can be generated with:

```
poetry run python manage.py dumpdata trackers --format=yaml --indent=2 > trackers/fixtures/[fixture-name].yaml
```
