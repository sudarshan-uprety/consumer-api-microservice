pipeline {
    agent any

    environment {
        PROD_ENV = 'ECOM_PROD_ENV'
        UAT_ENV = 'ECOM_UAT_ENV'
        DEV_ENV = 'ECOM_DEV_ENV'
        GRPC_ENV = 'ECOM_GRPC_ENV'
        PATH = 'ECOM_PATH'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Create .env File') {
            steps {
                script {
                    def envFileCredentialId = ""
                    
                    if (env.BRANCH_NAME == 'prod') {
                        envFileCredentialId = env.PROD_ENV
                    } else if (env.BRANCH_NAME == 'uat') {
                        envFileCredentialId = env.UAT_ENV
                    } else if (env.BRANCH_NAME == 'dev') {
                        envFileCredentialId = env.DEV_ENV
                    } else {
                        error "This branch does not have corresponding environment variables"
                    }
                    
                    // Use file credentials for all environments
                    withCredentials([file(credentialsId: envFileCredentialId, variable: 'ENV_FILE')]) {
                        sh 'cp $ENV_FILE .env'
                    }
                }
            }
        }

        stage('Sync Deployments with rsync') {
            steps {
                script {
                    // Using the credentials from your table
                    withCredentials([
                        string(credentialsId: 'HOST_IP', variable: 'SERVER_HOST'),
                        string(credentialsId: 'SERVER_USER', variable: 'SERVER_USER'),
                        file(credentialsId: 'SERVER_KEY', variable: 'SSH_KEY_PATH'),
                        string(credentialsId: 'SERVER_PORT', variable: 'SSH_PORT')
                    ]) {
                        // Username is often hardcoded or could be stored as another credential
                        def remoteUser = "oracle"  // Replace with your SSH username
                        def deploymentPath = "${env.ECOM_PATH}"
                        
                        sh """
                            rsync -avzr --delete -e "ssh -i \$SSH_KEY_PATH -p \$SSH_PORT" ./ \${SERVER_USER}@\${SERVER_HOST}:\${deploymentPath}${env.BRANCH_NAME}
                        """
                    }
                }
            }
        }

        stage('Start Docker Containers') {
            steps {
                script {
                    def composeUpCommand = ''
                    if (env.BRANCH_NAME == 'dev') {
                        composeUpCommand = 'sudo docker-compose up -d elasticsearch auth_db_dev auth_service_dev --build'
                    } else if (env.BRANCH_NAME == 'uat') {
                        composeUpCommand = 'sudo docker-compose up -d elasticsearch auth_db_uat auth_service_uat --build'
                    } else if (env.BRANCH_NAME == 'prod') {
                        composeUpCommand = 'sudo docker-compose up -d elasticsearch auth_db_prod auth_service_prod --build'
                    } else if (env.BRANCH_NAME == 'grpc') {
                        composeUpCommand = 'sudo docker-compose up -d elasticsearch auth_db_grpc auth_service_grpc --build'
                    } else {
                        error "Unexpected branch"
                    }

                    // Using the credentials to SSH into the server and run docker commands
                    withCredentials([
                        string(credentialsId: 'HOST_IP', variable: 'SERVER_HOST'),
                        file(credentialsId: 'SERVER_KEY', variable: 'SSH_KEY_PATH'),
                        string(credentialsId: 'SERVER_PORT', variable: 'SSH_PORT')
                    ]) {
                        def remoteUser = "oracle"  // Replace with your SSH username
                        def deploymentPath = "${env.ECOM_PATH}"
                        
                        sh """
                            ssh -i \$SSH_KEY_PATH -p \$SSH_PORT \${remoteUser}@\${SERVER_HOST} "cd \${deploymentPath}${env.BRANCH_NAME} && ${composeUpCommand} && sudo docker image prune -a --force"
                        """
                    }
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