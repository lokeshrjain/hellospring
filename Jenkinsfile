pipeline {
  agent any
  stages{
    stage('Checkout') {
      steps {
      checkout scm
      }
    }
  	stage('Build and Test') {
  	  steps {
       sh './mvnw clean install -DskipTests=true'
      }
  	}
  stage('deploy to staging') {
    environment {
      AWS_ACCESS_KEY_ID = credentials('jenkins-aws-secret-key-id')
      AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
      DEPLOYMENT = 'staging'
      AWS_DEFAULT_REGION = 'us-west-2'
    }
    steps {
      sh './bin/deploy_to_staging'
    }
  }
}
  options {
  timestamps()
  skipDefaultCheckout()
  }
}