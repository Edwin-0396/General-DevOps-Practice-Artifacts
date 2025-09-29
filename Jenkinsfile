pipeline {
    agent any

    options {
        ansiColor('xterm')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        IMAGE_NAME = 'parameta/devops-mvp'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
        REGISTRY_CREDENTIALS = 'docker-registry-credentials'
        KUBE_CONFIG_CREDENTIALS = 'kubeconfig-eks-cluster'
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python environment') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'python -m pip install -r requirements.txt -r requirements-dev.txt'
            }
        }

        stage('Static analysis') {
            steps {
                sh 'flake8 app app/tests'
            }
        }

        stage('Unit tests') {
            steps {
                sh 'mkdir -p build/test-results build/coverage'
                sh 'pytest --junitxml=build/test-results/pytest.xml --cov=app --cov-report=xml:build/coverage/coverage.xml'
            }
            post {
                always {
                    junit 'build/test-results/pytest.xml'
                    publishCoverage adapters: [coberturaAdapter('build/coverage/coverage.xml')]
                }
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build --pull --tag $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push to registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CREDENTIALS, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
                    sh 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                withKubeConfig([credentialsId: KUBE_CONFIG_CREDENTIALS]) {
                    sh 'kubectl apply -f k8s/'
                    sh 'kubectl set image deployment/parameta-devops-mvp app=$IMAGE_NAME:$IMAGE_TAG'
                    sh 'kubectl rollout status deployment/parameta-devops-mvp --timeout=2m'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
