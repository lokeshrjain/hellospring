pipeline {
  agent any
  stages{
  	stage('Build and Test') {
  	  steps {
       sh './mvnw clean install'
      }
  	}
  }
}