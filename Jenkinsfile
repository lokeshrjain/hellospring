pipeline {
  agent any
  tools {
    maven 'M3.6.0'
  }
  stages{
  	stage('Build and Test') {
  	  steps {
       sh 'mvn clean install'
      }
  	}
  }
}