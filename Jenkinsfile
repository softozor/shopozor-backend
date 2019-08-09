pipeline {
  agent {
    docker {
      image 'python:3.7'
    }
  }
  environment {
    REPORTS_FOLDER = 'junit-reports'
    // VENV = 'venv'
  }
  stages {
    stage('Virtual Environment Installation') {
      steps {
        withEnv(["HOME=$WORKSPACE, PATH=$HOME/.local/bin"]) {
          // sh "pip install virtualenv --user"
          // sh "$WORKSPACE/.local/bin/virtualenv $VENV"
          // sh ". $VENV/bin/activate && pip install dos2unix"
          // sh "python venv/lib/python3.7/site-packages/dos2unix.py scripts/install/install.sh scripts/install/install.sh"
          // sh "python venv/lib/python3.7/site-packages/dos2unix.py scripts/install/install-dev.sh scripts/install/install-dev.sh"
          // sh "chmod u+x ./scripts/install/*.sh"
          // sh ". $VENV/bin/activate && ./scripts/install/install.sh"
          // sh ". $VENV/bin/activate && ./scripts/install/install-dev.sh"
          sh "pip install pipenv --user"
          sh "pipenv install --user --deploy --dev"
        }
      }
    }
    stage('Performing acceptance tests') {
      environment {
        DATABASE_URL = credentials('postgres-credentials')
        DJANGO_SETTINGS_MODULE = 'features.settings'
        PYTHONPATH = "$PYTHONPATH:$WORKSPACE/saleor"
        JWT_EXPIRATION_DELTA_IN_DAYS = 30
        JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS = 360
        JWT_SECRET_KEY = 'test_key'
        JWT_ALGORITHM = 'HS256'
        SECRET_KEY = 'theSecretKey'
      }
      steps {
        // sh ". $VENV/bin/activate && python manage.py behave --junit --junit-directory $REPORTS_FOLDER --tags=\"~wip\""
        sh "python manage.py behave --junit --junit-directory $REPORTS_FOLDER --tags ~wip"
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
