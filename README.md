# New Bloodhound

## Getting the Bloodhound Code:

There is a reasonable chance that you are reading these instructions from a
copy of the source code that you have already placed on the computer that you
wish to install on. If this is the case you can skip on to the next section.

While in early development, the alternatives for getting the code include
checking out from [Subversion] with the following command:

```
svn checkout https://svn.apache.org/repos/asf/bloodhound/branches/bh_core_experimental/ bloodhound
```

or cloning with [Git] from the [Apache Bloodhound Github mirror] - the command
below should also check out the appropriate branch:

```
git clone --branch bh_core_experimental https://github.com/apache/bloodhound.git
```

With the commands as specified, both will place the code in the `bloodhound`
directory.

[Subversion]: https://subversion.apache.org/
[Git]: https://git-scm.com/
[Apache Bloodhound mirror]: https://github.com/apache/bloodhound
[Github]: https://github.com/

## Installing Python and Pipenv

Bloodhound core is currently written in [Python 3] and uses [Pipenv] for
looking after the python based dependencies.

It should be possible to install and run the core successfully with Python 3.6
or newer. You may find that versions from Python 3.4 work but this is not
currently tested and it is possible that Python features from newer versions
may sneak in.

The guide at <https://docs.python-guide.org/> gives good instructions for
installing Python on [Linux][Python on Linux], [MacOS][Python on MacOS] and
[Windows][Python on Windows].

Further information about pipenv is available at <https://docs.pipenv.org/>.

[Python 3]: https://docs.python.org/3/
[Pipenv]: https://pipenv.readthedocs.io/en/latest/
[Python on Linux]: https://docs.python-guide.org/starting/install3/linux/#install3-linux
[Python on MacOS]: https://docs.python-guide.org/starting/install3/osx/#install3-osx
[Python on Windows]: https://docs.python-guide.org/starting/install3/win/#install3-windows

## Preparing the Python environment

It should now be possible to use pipenv to install the rest of the project
dependencies and bloodhound itself. Note that the exactly required command may
depend on details like whether you have multiple versions of python available
but for most cases, the following should work. If in doubt, just be more
specific about the python version that you intend to use.

For the same directory as the `Pipfile` for the project run:

```
pipenv --python 3 install
```

## Setup

Although it will make the commands more verbose, where a command requires
the pipenv environment that has been created, we will use the `pipenv run`
command in preference to requiring that the environment is 'activated'.

The basic setup steps to get running are:

```
pipenv run python manage.py makemigrations trackers
pipenv run python manage.py migrate
```

The above will do the basic database setup.

Note that currently models are in flux and, for the moment, no support should
be expected for migrations as models change. This will change when basic
models gain stability.

## Running the development server:

```
pipenv run python manage.py runserver
```

Amongst the initial output of that command will be something like:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Currently there is not much to see at the specified location. More work has
been done on the core API. The following views may be of interest as you
explore:

 * http://127.0.0.1:8000/ticket/
 * http://127.0.0.1:8000/schema_view/

These paths are subject to change.

## Unit Tests

Unit tests are currently being written with the standard unittest framework.
This may be replaced with pytest.

Running the tests require a little extra setup:

```
pipenv install --dev
```

after which the tests may be run with the following command:

```
pipenv run python manage.py test
```

## Integration Tests

The [Selenium] tests currently require that Firefox is installed and
[geckodriver] is also on the path. If you 
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
pipenv run python functional_tests.py
```

There are currently not many tests - those that are there are in place to test
the setup above and assume that there will be useful tests in due course.

[Selenium]: https://selenium.dev/
[geckodriver]: https://firefox-source-docs.mozilla.org/testing/geckodriver/

## Development notes:

Fixtures for tests when required can be generated with:

```
pipenv run python manage.py dumpdata trackers --format=yaml --indent=2 > trackers/fixtures/[fixture-name].yaml
```
