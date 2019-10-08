# shopozor-backend


## Build statuses

[![Acceptance Build Status](http://shopozor-ci.hidora.com/buildStatus/icon?job=shopozor-backend-acceptance&subject=acceptance%20tests)](http://shopozor-ci.hidora.com/job/shopozor-backend-acceptance/)
[![Unit Build Status](http://shopozor-ci.hidora.com/buildStatus/icon?job=shopozor-backend-unit&subject=unit%20tests)](http://shopozor-ci.hidora.com/job/shopozor-backend-unit/)

## Docker images

### Development

As a frontend developer, you might need to connect your application to the Shopozor's backend server. The development docker image is produced manually upon every PR merging into the `dev` branch. In order to run the server,
1. clone this repo
```
git clone https://github.com/shopozor/backend
cd backend
git submodule init
git submodule update
```
2. run
```
docker-compose up
```
at the root of that clone
3. setup the database with
```
docker exec -it $(docker ps -aqf "name=backend_web") python3 manage.py migrate
```
at the root of that clone.

## Continuous integration

We were not able to display the usual cucumber reports in Jenkins for this repository because the `behave` reports are not compatible with the `cucumber` reports (see e.g. [this reference](https://www.bountysource.com/issues/6638934-behave-json-reports-are-incompatible-with-cucumber-ones)). Therefore our `Jenkinsfile` makes use of the `junit` framework to output acceptance test results.

## Pull requests

### Workflow

* All Softozor members are whitelisted
* When a white-listed author opens a PR, she is triggering the corresponding unit and acceptance tests automatically
* When a white-listed member updates a PR, she is triggering the corresponding unit and acceptance tests again
* When a non-whitelisted member opens a PR, the builder will publish the question `Can one of the admins verify this patch?` to the PR's comment; in that case, one of Softozor's admins can

  * comment `ok to test` to accept the PR for testing
  * comment `test this please` for one time test run
  * comment `add to whitelist` to add the PR's author to the whitelist

### Useful build commands

You can use the following commands in your comments:

* `retest this please`: this runs the unit and acceptance tests again

## Development's instructions

### Setup the Shopozor software

1. Clone the repository
```
git clone https://github.com/softozor/shopozor-backend
```
2. Init and update all the submodules
```
cd shopozor-backend
git submodule init
git submodule update
```
In particular, [saleor software](https://github.com/mirumee/saleor) will then be accessible at the latest release we granted access to.

3. Create virtual environment
```
virtualenv venv
```
4. Install dependencies
```
./scripts/install/install.sh
./scripts/install/install-dev.sh
```

5. Activate the pre-commit hooks

```
./scripts/activate-hooks.sh
```

That activates pre-commit hooks for the backend code as well as for the graphql queries repo and fixtures repo.

6. Add the relevant environment variables to the virtual environment (in the file `venv/bin/activate`):
```
export WORKSPACE=<full-path-to-repo>
export PYTHONPATH=$PYTHONPATH:$WORKSPACE/saleor
export SECRET_KEY=hahahaha
export JWT_EXPIRATION_DELTA_IN_DAYS=30
export JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS=360
export JWT_SECRET_KEY='test_key'
export JWT_ALGORITHM='HS256'
```
7. Everytime you need to run a shopozor command, you will need to have activated your virtual environment:
```
cd shopozor-backend
source venv/bin/activate
```

Make sure that the path to `saleor` module is correctly displayed by the following command in the python shell:

1. run the python shell
```
python manage.py shell
```
2. double-check the python path:
```
import sys
for path in sys.path:
    print(path)
```

### Setup the PostgreSQL database

Following [this advice](https://tecadmin.net/install-postgresql-server-on-ubuntu/), you do

```
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib
```

### Setup the Shopozor PostgreSQL database

First, you create the database user and the database:
```
sudo -u postgres psql -c "CREATE ROLE saleor PASSWORD 'saleor' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"
sudo -u postgres psql -c "CREATE DATABASE saleor OWNER saleor ENCODING 'utf-8' TEMPLATE template0;"
```
Second, you perform Django's database migration:
```
cd shopozor-backend
. ./venv/bin/activate
python manage.py migrate
```

### Getting started

To get started, you can access the shopozor's GraphQL playground. To make it happen, you need to
```
sudo /etc/init.d/postgresql start
cd shopozor-backend
. ./venv/bin/activate
python manage.py runserver
```
Then you browse `http://localhost:8000/graphql` and discover the Shopozor's GraphQL playground.

### Configuring Visual Studio Code

First, you need to [install VS Code](https://linuxize.com/post/how-to-install-visual-studio-code-on-ubuntu-18-04/). The relevant configuration is set in [VS Code settings file](.vscode/settings.json). In addition to that, you might also want to install the extensions we find useful:
```
cd shopozor-backend
./.vscode/install-extensions.sh
```
To start the shopozor-backend so that it recognizes all the necessary python module, do this:
```
cd shopozor-backend
. ./venv/bin/activate
code . &
```
In addition to that, the first time you open the project, you might need to specify the python interpreter as explained [here](https://code.visualstudio.com/docs/python/python-tutorial#_select-a-python-interpreter). If you work under Windows with WSL, follow [this advice](https://devblogs.microsoft.com/python/remote-python-development-in-visual-studio-code/).

Some of the Visual studio code settings are really user-specific. For example, the path to the python interpreter or the terminal to be used is not something we want to share across all the team. An example of user-specific settings is provided [here](.vscode/user-settings.json) that uses a python interpreter through a WSL terminal. Under Windows 10, such settings are usually stored under `C:\Users\<username>\AppData\Roaming\Code\User\settings.json`.

### Testing saleor

The purpose of the `shopozor-backend` project is to provide the Shopozor's frontends with a backend. In particular, this means that we don't care at all about saleor's frontend developments. However, it can be that you need to run saleor's tests for some reasons. In that case, you will need to

1. Install `saleor`'s third-party dependencies (cf. method `installSaleorDependencies` of our [CI/CD installation manifest](https://github.com/softozor/shopozor-ci/blob/master/manifest.jps))
```
sudo apt install -y build-essential python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```
2. Build `saleor`'s frontend software (cf. [unit testing pipeline](./unit_testing.groovy))
```
cd shopozor-backend/saleor
npm i
npm run build-assets
npm run build-emails
```
3. Run `saleor`'s unit tests (cf. [unit testing pipeline](./unit_testing.groovy)):
```
export DJANGO_SETTINGS_MODULE=saleor.settings
py.test -ra
```

### Testing the Shopozor

Running the Shopozor backend acceptance tests do not require any frontend installation. [Their specification](https://github.com/softozor/shopozor-backend/blob/dev/features) is written in Gherkin language. To run them, you can run the following commands (cf. [acceptance testing pipeline](Jenkinsfile)):
```
cd shopozor-backend
. ./venv/bin/activate
python manage.py behave --settings features.settings --keepdb --tags ~wip
```
You can get rid of the `--tags` option if you want to run the features that are "work in progress" too.
