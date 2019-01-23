import boto3
import argparse
from operator import itemgetter

ecs = boto3.client('ecs')
"""Client interface for ECS"""


elbv2 = boto3.client('elbv2')

def delete_balanced_service(target_group_arn,service_name,cluster_name,rule_arn):
    try:
        print("deleting rule " + rule_arn)
        elbv2.delete_rule(
            RuleArn=rule_arn
        )
        print("deleting target group " + target_group_arn)
        elbv2.delete_target_group(
            TargetGroupArn=target_group_arn
        )
        print("deleting service " + service_name)
        elbv2.delete_service(
             cluster=cluster_name,
             service=service_name,
             force=True
        )
    except:
        print("clean up exceuted with partial error")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='delete service balanced from ECS.',
    )
    parser.add_argument('--listener-arn',
        dest='listener_arn',
        type=str,
        help=("Name of the listener arn, which will be deleted."),
    )
    parser.add_argument('--target-group-arn',
        dest='target_group_arn',
        type=str,
        default='my-tg',
        help=("Name of the target group, which will be deleted."),
    )
    parser.add_argument('--service-name',
        dest='service_name',
        type=str,
        default='my-service',
        help=("Name of the ECS service which will be deleted."),
    )
    parser.add_argument('--cluster-name',
        dest='cluster_name',
        type=str,
        default='my-cluster',
        help=("Name of the ECS cluster which will be deleted."),
    )

    args = parser.parse_args()
    print(" Arguments: " + args)
    delete_balanced_service(
      args.target_group_arn,
      args.service_name,
      args.cluster_name,
      args.rule_arn,
    )