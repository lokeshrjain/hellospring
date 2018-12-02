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
       sh './mvnw clean install'
      }
  	}
stage('deploy to staging') {
steps {
  sh './bin/deploy_to_staging'
}

}
  options {
  timestamps()
  skipDefaultCheckout()
  }
}