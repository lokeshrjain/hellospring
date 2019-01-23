import boto3
import argparse
from operator import itemgetter
import deleteService

ecs = boto3.client('ecs')
"""Client interface for ECS"""


elbv2 = boto3.client('elbv2')
"""Client interface for ELBv2"""


def create_balanced_service(
  cluster_name,
  family,
  load_balancer_name,
  protocol,
  port,
  container_name,
  vpc_id,
  ecs_service_role,
  service_name,
  task_amount,
):
    """Create a service and return it.

    Positional parameters:n
          cluster_name -- Name of the cluster
                family -- Family of the task definition
    load_balancer_name -- Name of the load balancer
     load_balancer_arn -- ARN of the load balancer
              protocol -- Protocol of the exposed port
                  port -- Number of the exposed port
        container_name -- Name of the container the port belongs to
                vpc_id -- ID of the current VPC
      ecs_service_role -- ARN of the `ecsServiceRole' role
          service_name -- Name of the service
           task_amount -- Desired amount of tasks
    """
    #initialize variables
    listener_arn=""
    rule_arn=""
    load_balancer_arn=""
    target_group_arn=""

    try:
        load_balancers=elbv2.describe_load_balancers(
            Names=['ecs-c-LoadB-C68ATIIZJX04']
        )

        #check whether we have ALB
        if load_balancers['LoadBalancers']:
            load_balancer_arn=load_balancers['LoadBalancers'][0]['LoadBalancerArn']
        else:
            #create a load balancer
            print("create a load balancer")

        print("load_balancer_arn :" +load_balancer_arn)
        target_group_arn = elbv2.create_target_group(
            Protocol=protocol,
            Port=port,
            VpcId=vpc_id,
            Name='{}-{}'.format(family,'tg'),
            HealthCheckPath='/health',
        )['TargetGroups'][0]['TargetGroupArn']

        print("target_group_arn :"+ target_group_arn)

        listeners = elbv2.describe_listeners(
            LoadBalancerArn=load_balancer_arn,
            PageSize=10
        )
        #check and assign listener json array.
        if listeners['Listeners']:
            listener_arn=listeners['Listeners'][0]['ListenerArn']

        print("listener_arn :" +listener_arn)
        #check whether we have lintener on target group
        if listener_arn:
            next_priority=elbv2.describe_rules(
                ListenerArn=listener_arn,
                PageSize=100
            )
            #filter the default priority
            priorities = list(filter(lambda k:k['Priority'] != 'default', next_priority['Rules']))
            max_priority='0'
            print(priorities)
            #get the max priority for rule

            #In python you can only list once then filter will become empty.
            if priorities:
                print("inside :" +max_priority)
                max_priority=max(priorities, key=lambda k:k['Priority'])['Priority']

            print("max_priority "+max_priority)
            print("Creating new rule...")
            rule_arn=elbv2.create_rule(
                ListenerArn=listener_arn,
                Conditions=[
                        {
                            'Field': 'path-pattern',
                            'Values': [
                                '/*',
                            ]
                        },
                    ],
                    Priority=int(max_priority)+1,
                    Actions=[
                            {
                                'Type': 'forward',
                                'TargetGroupArn':target_group_arn
                             }
                             ]
            )['Rules'][0]['RuleArn']
            print("rule_arn :" + rule_arn)
        # aws elbv2 create-rule --listener-arn $api_elb_listener_arn  --priority $next_priority --conditions Field=path-pattern,Values="$mapped_path/*" --actions Type=forward,TargetGroupArn=$TG_ARN
        #This is going to be one time activity as we can add more rules with existing ALB base on the base path of api.
        else:
            print("Creating new listner...")
            elbv2.create_listener(
                LoadBalancerArn=load_balancer_arn,
                Protocol=protocol,
                Port=80,
                DefaultActions=[
                    {
                        'Type': 'forward',
                        'TargetGroupArn': target_group_arn,
                    }
                ],
            )

        print("Creating new service...")
        return ecs.create_service(
            cluster=cluster_name,
            serviceName=service_name,
            taskDefinition=family,
            role=ecs_service_role,
            loadBalancers=[
                {
                    'targetGroupArn': target_group_arn,
                    'containerName': container_name,
                    'containerPort': port,
                }
            ],
            desiredCount=task_amount,
        )
    except Exception as e:
        print("Something went wrong...clean up " + e)
        print("rule_arn " + rule_arn)
        print("target_group_arn " + target_group_arn)
        print("service_name " + service_name)
        print("cluster_name " + cluster_name)
        deleteService.delete_balanced_service(
                            target_group_arn,
                            service_name,
                            cluster_name,
                            rule_arn
                          )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Setup clustered, load balanced ECS tasks.',
    )
    parser.add_argument('--task-count',
        dest='task_count',
        type=int,
        default=1,
        help=("Number of tasks to be run on the cluster. Will be balanced "
              "between all container instances."),
    )
    parser.add_argument('--task-family-name',
        dest='family_name',
        type=str,
        default='my-family',
        help=("Name of the service family. Services are versionned, and "
              "versions of the same service must have the same family name."),
    )
    parser.add_argument('--load-balancer-name',
        dest='load_balancer_name',
        type=str,
        default='my-lb',
        help=("Name of the load balancer which will be created."),
    )
    parser.add_argument('--service-protocol',
        dest='protocol',
        type=str,
        choices=['HTTP', 'TCP', 'UDP'],
        required=True,
        help=("Protocol used by the exposed port."),
    )
    parser.add_argument('--service-port',
        dest='port',
        type=int,
        required=True,
        help=("Number of the exposed port."),
    )
    parser.add_argument('--service-container',
        dest='container_name',
        type=str,
        required=True,
        help=("Name of the container th=hellospringe port belongs to. This is the same as "
              "the key under which the container is described in the "
              "docker-compose file."),
    )
    parser.add_argument('--service-name',
        dest='service_name',
        type=str,
        default='my-service',
        help=("Name of the ECS service which will be created."),
    )
    parser.add_argument('--vpc_id',
        dest='vpc_id',
        type=str,
        help=("vpc_id to the docker-compose file to be deployed."),
    )
    parser.add_argument('--ecs_service_role',
        dest='ecs_service_role',
        type=str,
        help=("ecs_service_role to the docker-compose file to be deployed."),
    )
    parser.add_argument('--cluster-name',
        dest='cluster_name',
        type=str,
        help=("cluster_name to the docker-compose file to be deployed."),
    )

    args = parser.parse_args()
    print(args)
    create_balanced_service(
      args.cluster_name,
      args.family_name,
      args.load_balancer_name,
      args.protocol,
      args.port,
      args.container_name,
      args.vpc_id,
      args.ecs_service_role,
      args.service_name,
      args.task_count,
    )