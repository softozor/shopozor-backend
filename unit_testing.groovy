// TODO: the best option here is to go for a pipeline with Dockerfile:
// https://jenkins.io/doc/book/pipeline/docker/#dockerfile
pipeline {
  agent {
    docker {
      image 'python:3.7'
    }
  }
  environment {
    REPORTS_FOLDER = 'junit-reports'
    PIPENV_VENV_IN_PROJECT = "enabled"
    PATH = "$PATH:$WORKSPACE/.venv/bin:$WORKSPACE/.local/bin"
  }
  stages {
    stage('Virtual Environment Installation') {
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "pip install pipenv --user"
          sh "$WORKSPACE/.local/bin/pipenv install --deploy --dev"
        }
      }
    }
    // stage('Build saleor frontend') {
    //   steps {
    //     withEnv(["HOME=$WORKSPACE"]) {
    //       sh "cd saleor && npm i && npm run build-assets && npm run build-emails"
    //     }
    //   }
    // }
    // stage('Performing saleor unit tests') {
    //   environment {
    //     DATABASE_URL = credentials('postgres-credentials')
    //     DJANGO_SETTINGS_MODULE = 'tests.settings'
    //     PYTHONPATH = "$PYTHONPATH:$WORKSPACE/saleor"
    //   }
    //   steps {
    //     withEnv(["HOME=$WORKSPACE"]) {
    //       sh "cd saleor && pipenv run $WORKSPACE/.venv/bin/pytest -ra --junitxml=$REPORTS_FOLDER/saleor-unit-tests.xml"
    //     }
    //   }
    // }
    stage('Performing shopozor unit tests') {
      environment {
        DATABASE_URL = credentials('postgres-credentials')
        DJANGO_SETTINGS_MODULE = 'unit_tests.settings'
        PYTHONPATH = "$PYTHONPATH:$WORKSPACE/saleor"
        SECRET_KEY = 'theSecretKey'
      }
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "$WORKSPACE/.local/bin/pipenv run python manage.py test"
        }
      }
    }
  }
  post {
    always {
      script {
         junit "**/$REPORTS_FOLDER/*.xml"
      }
    }
  }
}
