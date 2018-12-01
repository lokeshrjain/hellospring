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
  }
  options {
  timestamps()
  skipDefaultCheckout()
  }
}