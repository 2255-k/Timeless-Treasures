pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Django Validation') {
            steps {
                sh '''
                    docker run --rm \
                      -e PYTHONDONTWRITEBYTECODE=1 \
                      -e PYTHONUNBUFFERED=1 \
                      -v "/var/lib/docker/volumes/jenkins_home/_data/workspace/Timeless-Tressure:/app" \
                      -w /app \
                      python:3.12-slim \
                      sh -ec '
                        python -m venv /tmp/venv
                        /tmp/venv/bin/pip install --no-cache-dir -r requirements.txt
                        /tmp/venv/bin/python manage.py check
                        /tmp/venv/bin/python manage.py makemigrations --check --dry-run
                        /tmp/venv/bin/python manage.py test
                        /tmp/venv/bin/python manage.py collectstatic --noinput
                      '
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t timeless-treasures:${BUILD_NUMBER} .'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Django validation and Docker image build completed.'
        }
        failure {
            echo 'FAILED: Check the Console Output to identify the failing stage.'
        }
    }
}
