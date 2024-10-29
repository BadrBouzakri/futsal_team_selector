pipeline {
    environment { 
        // Déclaration des variables d'environnement globales
        DOCKER_ID = "bouzakri" // Remplacez par votre identifiant Docker
        DOCKER_IMAGE = "foot_app"
        DOCKER_TAG = "v.${BUILD_ID}.0" // Tag des images avec l'ID de build pour l'incrémentation automatique
    }
    agent any // Jenkins peut sélectionner n'importe quel agent disponible

    stages {
        stage('Docker Build') { 
            steps {
                script {
                    sh '''
                    docker rm -f jenkins || true
                    docker build -t $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG .
                    sleep 6
                    '''
                }
            }
        }

        stage('Docker Run') { 
            steps {
                script {
                    sh '''
                    docker run -d -p 4545:4545 --name jenkins $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG
                    sleep 10
                    '''
                }
            }
        }

        stage('Test Acceptance') { 
            steps {
                script {
                    sh '''
                    curl localhost:4545
                    '''
                }
            }
        }

        stage('Docker Push') { 
            environment {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS") // Récupération du mot de passe Docker Hub depuis les credentials Jenkins
            }
            steps {
                script {
                    sh '''
                    docker login -u $DOCKER_ID -p $DOCKER_PASS
                    docker push $DOCKER_ID/$DOCKER_IMAGE:$DOCKER_TAG
                    '''
                }
            }
        }

        stage('Deploiement en dev') {
            environment {
                KUBECONFIG = credentials("config") // Récupération de kubeconfig depuis les credentials Jenkins
            }
            steps {
                script {
                    sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/ingress.yaml
                    kubectl apply -f k8s/pv.yaml
                    kubectl apply -f k8s/pvc.yaml
                    '''
                }
            }
        }

        stage('Deploiement en staging') {
            environment {
                KUBECONFIG = credentials("config")
            }
            steps {
                script {
                    sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/ingress.yaml
                    kubectl apply -f k8s/pv.yaml
                    kubectl apply -f k8s/pvc.yaml
                    '''
                }
            }
        }

        stage('Deploiement en prod') {
            environment {
                KUBECONFIG = credentials("config")
            }
            steps {
                script {
                    // Créer un bouton d'approbation avec un délai d'expiration de 15 minutes
                    def userInput = input(
                        id: 'userInput', message: 'Do you want to deploy in production?', ok: 'Yes',
                        parameters: [
                            choice(name: 'Approval', choices: ['Yes', 'No'], description: 'Select Yes to proceed')
                        ]
                    )

                    // Vérification de l'approbation de l'utilisateur pour le déploiement en production
                    if (userInput == 'Yes') {
                        echo "Déploiement en production approuvé, exécution du déploiement..."
                        sh '''
                        kubectl apply -f k8s/deployment.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl apply -f k8s/ingress.yaml
                        kubectl apply -f k8s/pv.yaml
                        kubectl apply -f k8s/pvc.yaml
                        '''
                    } else {
                        echo "Déploiement en production annulé par l'utilisateur."
                    }
                }
            }
        }
    }
}
