pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devanshpandey21/flask-currency-converter'
        IMAGE_TAG = "${env.BUILD_NUMBER}"

        // Ensure this name matches the one configured under: 
        // Jenkins > Manage Jenkins > Configure System > SonarQube installations
        SONARQUBE_SERVER = 'SonarQube'
        SONAR_PROJECT_KEY = 'flask-currency-converter-project'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/LearnerDevansh/flask-currency-converter.git'
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SONAR_AUTH_TOKEN = credentials('sonarqube-creds')
            }
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    withEnv(["PATH+SCANNER=${tool 'MySonarQubeScanner'}/bin"]) {
                        bat """
                            sonar-scanner ^
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} ^
                            -Dsonar.sources=. ^
                            -Dsonar.login=${SONAR_AUTH_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t \"$IMAGE_NAME:$IMAGE_TAG\" ."
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        sh "echo \"$DOCKER_PASS\" | docker login -u \"$DOCKER_USER\" --password-stdin"
                        sh "docker push \"$IMAGE_NAME:$IMAGE_TAG\""
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([file(credentialsId: 'aws-kubeconfig', variable: 'KUBECONFIG')]) {
                    bat '''
                        kubectl apply -f k8s\\dev\\deployment.yaml ^
                        && kubectl apply -f k8s\\dev\\service.yaml
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Docker image pushed and deployed successfully!'
        }
        failure {
            echo '❌ Build, push, or deploy failed.'
        }
    }
}
