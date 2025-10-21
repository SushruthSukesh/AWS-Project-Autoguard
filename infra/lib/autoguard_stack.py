from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_iam as iam,
    aws_events as events,
    aws_events_targets as targets,
    Duration,
    RemovalPolicy,
    Aws,
)
from constructs import Construct
import os

class AutoGuardStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket for artifacts and audit logs
        audit_bucket = s3.Bucket(self, "AutoGuardAuditBucket",
                                removal_policy=RemovalPolicy.DESTROY,
                                auto_delete_objects=True)

        # DynamoDB table for agent memory / incidents
        memory_table = ddb.Table(self, "AgentMemory",
                                 partition_key=ddb.Attribute(name="incident_id", type=ddb.AttributeType.STRING),
                                 removal_policy=RemovalPolicy.DESTROY)

        # IAM role for Lambdas
        lambda_role = iam.Role(self, "AutoGuardLambdaRole",
                               assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        # Add limited CostExplorer permissions, CloudWatch read, EC2 read/stop/tag, etc. (scope down in prod)
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess"))

        # Remediator Lambda (safe operations)
        remediator = _lambda.Function(self, "RemediatorFunction",
                                      runtime=_lambda.Runtime.PYTHON_3_11,
                                      handler="remediator.lambda_handler",
                                      code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), "../../agentcore/tools")),
                                      role=lambda_role,
                                      timeout=Duration.seconds(30))

        # Simple scheduled rule to run a periodic check (demo)
        rule = events.Rule(self, "PeriodicCheckRule",
                           schedule=events.Schedule.rate(Duration.minutes(5)))
        rule.add_target(targets.LambdaFunction(remediator))
