pipeline {
    agent {
        node {
            label ''
            retries 2
        }
    }

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
                      -v "$WORKSPACE:/app" \
                      -w /app \
                      python:3.12-slim \
                      sh -ec '
                        python -m venv /tmp/venv
                        /tmp/venv/bin/pip install --no-cache-dir -r requirements.txt
                        /tmp/venv/bin/python manage.py check
                        /tmp/venv/bin/python manage.py makemigrations --check --dry-run
                        /tmp/venv/bin/python manage.py test
                        /tmp/venv/bin/python manage.py collectstatic --noinput

