# Traffic shift examples

These examples assume blue is version 1 and green is version 2.

## All at once

Deployment config:

```text
CodeDeployDefault.ECSAllAtOnce
```

Timeline:

```text
00:00  green is healthy
00:00  production traffic changes from 100% blue to 100% green
```

Use this for dev/test or low-risk services.

## Canary

Deployment config:

```text
CodeDeployDefault.ECSCanary10Percent5Minutes
```

Timeline:

```text
00:00  90% blue, 10% green
05:00  0% blue, 100% green
```

This is useful when you want to test the new task definition with a small
amount of real traffic before switching everyone.

## Linear

Deployment config:

```text
CodeDeployDefault.ECSLinear10PercentEvery3Minutes
```

Timeline:

```text
00:00  90% blue, 10% green
03:00  80% blue, 20% green
06:00  70% blue, 30% green
09:00  60% blue, 40% green
12:00  50% blue, 50% green
15:00  40% blue, 60% green
18:00  30% blue, 70% green
21:00  20% blue, 80% green
24:00  10% blue, 90% green
27:00  0% blue, 100% green
```

This is useful when you want a slower rollout and more time for alarms to catch
problems.

## Rollback idea

If CloudWatch alarms fire or health checks fail during the deployment,
CodeDeploy can stop shifting traffic and send users back to blue.

That is the main reason blue/green is safer than simply replacing all tasks in
place.
