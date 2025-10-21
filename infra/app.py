#!/usr/bin/env python3
import aws_cdk as cdk
from lib.autoguard_stack import AutoGuardStack

app = cdk.App()
AutoGuardStack(app, "AutoGuardStack", env=cdk.Environment(account=cdk.Aws.ACCOUNT_ID, region=cdk.Aws.REGION))
app.synth()
