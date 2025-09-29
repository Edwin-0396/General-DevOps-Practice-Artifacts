pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
        IMAGE_NAME = 'parameta/devops-mvp'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit tests') {
            steps {
                sh 'python -m unittest discover -s app/tests'
            }
        }

        stage('Build Docker image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push to registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-registry-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig-eks-cluster']) {
                    sh 'kubectl apply -f k8s/'
                    sh 'kubectl set image deployment/parameta-devops-mvp app=$IMAGE_NAME:$IMAGE_TAG'
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
