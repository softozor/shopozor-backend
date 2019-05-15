pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  } 
  environment {
    REPORTS_FOLDER = 'junit-reports'
    VENV = 'venv'
  }
  stages {
    stage('Virtual Environment Installation') {
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "pip install virtualenv --user"
          sh "$WORKSPACE/.local/bin/virtualenv $VENV"
          sh "chmod u+x ./scripts/install/*.sh"
          sh ". $VENV/bin/activate && ./scripts/install/install.sh"
          sh ". $VENV/bin/activate && ./scripts/install/install-dev.sh"
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
        sh ". $VENV/bin/activate && python manage.py behave --junit --junit-directory $REPORTS_FOLDER --tags=\"~wip\""
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
