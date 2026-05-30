# CodeDeploy with ECS: practical blue/green example

This folder is a learning example for how CodeDeploy deploys a new ECS task
definition.

The big idea:

1. You already have an ECS service running version 1 of your container.
2. You build and push version 2 of the container image to ECR.
3. You register a new ECS task definition revision that points to version 2.
4. CodeDeploy creates a replacement ECS task set, called green.
5. The load balancer shifts traffic from the old task set, called blue, to green.
6. If alarms and health checks pass, green becomes production and blue is removed.

## Files in this example

| File | Purpose |
| --- | --- |
| `app/app.py` | Tiny HTTP app that shows its version. |
| `Dockerfile` | Container image for the app. |
| `taskdef.json` | ECS task definition template. CodePipeline usually replaces `<IMAGE1_NAME>`. |
| `appspec.yaml` | CodeDeploy ECS AppSpec file. This points CodeDeploy to the task definition and container port. |
| `buildspec.yml` | Example CodeBuild file that builds the image and emits `taskdef.json` plus `appspec.yaml`. |
| `traffic-shift-examples.md` | Timeline examples for linear, canary, and all-at-once. |

## What Blue and Green look like

Assume your ECS service is currently running this image:

```text
123456789012.dkr.ecr.us-east-1.amazonaws.com/demo-app:v1
```

That is blue.

Now you build this image:

```text
123456789012.dkr.ecr.us-east-1.amazonaws.com/demo-app:v2
```

That becomes green. CodeDeploy does not mutate the old running tasks. It starts a
replacement task set using the new task definition, waits for it to become
healthy behind the load balancer, then shifts traffic to it.

## Important AWS resources

For a real deployment, you need:

- ECS cluster
- ECS service using deployment controller `CODE_DEPLOY`
- Application Load Balancer
- Two target groups: one for blue, one for green
- Production listener, usually port 80 or 443
- Optional test listener, for example port 8080
- CodeDeploy application with compute platform `ECS`
- CodeDeploy deployment group connected to the ECS service and the two target groups

## Example traffic policies

Use one of these on the CodeDeploy deployment group:

```text
CodeDeployDefault.ECSAllAtOnce
CodeDeployDefault.ECSCanary10Percent5Minutes
CodeDeployDefault.ECSCanary10Percent30Minutes
CodeDeployDefault.ECSLinear10PercentEvery3Minutes
CodeDeployDefault.ECSLinear10PercentEvery10Minutes
```

Example:

```text
CodeDeployDefault.ECSCanary10Percent5Minutes
```

CodeDeploy sends 10% of production traffic to green first. If the app stays
healthy for 5 minutes, CodeDeploy sends 100% of traffic to green.

## How the deployment artifact works

For ECS blue/green, CodeDeploy needs an AppSpec file like this:

```yaml
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: <TASK_DEFINITION>
        LoadBalancerInfo:
          ContainerName: demo-app
          ContainerPort: 80
```

In a real CodePipeline deployment, `<TASK_DEFINITION>` is replaced with the ARN
of the newly registered task definition revision.

## Mental model

```text
Before deployment

Users -> ALB listener -> blue target group -> ECS tasks using taskdef:1

During deployment

Users -> ALB listener -> blue target group  -> taskdef:1
                    \-> green target group -> taskdef:2

After successful deployment

Users -> ALB listener -> green target group -> ECS tasks using taskdef:2
```

## Official docs

- ECS blue/green deployments with CodeDeploy:
  https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-bluegreen.html
- CodeDeploy deployment configurations:
  https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html
- ECS deployment workflow in CodeDeploy:
  https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-steps-ecs.html
