pipeline {
    agent { label 'production-agent' }
    
    environment {
        DOCKER_HUB_CRED = 'docker-hub-credentials'
        DEPLOY_HOST = '192.168.0.221'
        DEPLOY_USER = 'deployer'
        VERSION = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Hircine01/jenkins.git'
            }
        }
        
        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKER_HUB_CRED, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }
        
        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh "docker build -t hircine01/jenkins-backend:${VERSION} ."
                    sh "docker tag hircine01/jenkins-backend:${VERSION} hircine01/jenkins-backend:latest"
                }
            }
        }
        
        stage('Build Nginx') {
            steps {
                dir('nginx') {
                    sh "docker build -t hircine01/jenkins-nginx:${VERSION} ."
                    sh "docker tag hircine01/jenkins-nginx:${VERSION} hircine01/jenkins-nginx:latest"
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh "docker push hircine01/jenkins-backend:${VERSION}"
                sh "docker push hircine01/jenkins-backend:latest"
                sh "docker push hircine01/jenkins-nginx:${VERSION}"
                sh "docker push hircine01/jenkins-nginx:latest"
            }
        }
        
        stage('Deploy to Server') {
            steps {
                sshagent(credentials: ['deploy-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                            mkdir -p /opt/jenkins-demo &&
                            cd /opt/jenkins-demo &&
                            
                            cat > docker-compose.yml << "EOF"
                            $(cat docker-compose.yml)
                            EOF
                            
                            export VERSION=${VERSION}
                            docker-compose pull
                            docker-compose up -d --force-recreate
                            docker system prune -f
                            
                            echo "✅ Deployment successful!"
                            echo "App is running at http://${DEPLOY_HOST}"
                        '
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "✅ Pipeline completed! Version: ${VERSION}"
            echo "App: http://${DEPLOY_HOST}"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
        always {
            sh 'docker logout'
        }
    }
}