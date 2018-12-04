#!/usr/bin/env bash


# more bash-friendly output for jq
#JQ="jq --raw-output --exit-status"



## family is task definition. cluster is cluster name and service is the service name on cluster
FAMILY="hellospring"
SERVICE="hellospring-web"
CLUSTER_NAME="shopalitic-ecs-cluster"
AWS_DEFAULT_REGION="us-west-2"
#ROLE_ARN=arn:aws:iam::$AWS_ACCOUNT_ID:role/nameofrole



env_staging(){
#Define env variables here
CLUSTER_NAME="shopalitic-ecs-cluster"
}

env_production(){
#Define env variables here
CLUSTER_NAME="shopalitic-ecs-cluster"
}


build_contacts_taskdef(){

if [ "$DEPLOY_NAME" = "production" ]; then
    #echo "Setting production env variables"
    env_production
else
    #echo "Setting staging env variables"
    env_staging
fi

        task_template='{
        "family": "'"$FAMILY"'",
            "containerDefinitions": [
        {
            "name": "'"$FAMILY"'",
            "image": "132522811272.dkr.ecr.us-west-2.amazonaws.com/shopalitic/hellospring:latest-staging",
            "essential": true,
            "memory": 512,
            "cpu": 512,
            "portMappings": [
                {
                    "containerPort": 8081,
                    "hostPort": 8081
                }
            ],
            "environment": [
                {
                    "name": "ENV",
                    "value": "staging"
                }
            ],

            "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "'"/$FAMILY"'",
                        "awslogs-region": "'"$AWS_DEFAULT_REGION"'",
                        "awslogs-stream-prefix": "'"$FAMILY"'"
                    }
            }
        }
    ]}'


    task_def=$(printf "$task_template" )
    echo $task_def
}

build_contacts_taskdef

