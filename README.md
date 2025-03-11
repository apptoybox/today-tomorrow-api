# Today Tomorrow API

A simple FastAPI application that provides endpoints for getting today's and tomorrow's dates in PDT timezone.

## Installation

```bash
pip install --requirement requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Endpoints

- `/today` - Returns today's date in PDT timezone
- `/tomorrow` - Returns tomorrow's date in PDT timezone
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)

## Open ID Connect Authentication

GitHub Action will use the Open ID Connect provider to authenticate with AWS STS. The Open ID Connect provider is created using the following command:

1. Create an OIDC provider

```bash
aws iam create-open-id-connect-provider --url "https://token.actions.githubusercontent.com" --thumbprint-list "6938fd4d98bab03faadb97b34396831e3780aea1" --client-id-list "sts.amazonaws.com"
```
2. Draft the OIDC policy in the file `oidc-policy.json`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::264318998405:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:apptoybox/today-tomorrow-api:*"
                },
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
```


3. Create IAM Role
```bash
aws iam create-role --role-name GitHubAction-AssumeRoleWithAction --assume-role-policy-document file://oidc-policy.json
```

4. Draft a policy that allows the role to push to ECR in the file `ecr-policy.json`

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [ "ecr:GetAuthorizationToken" ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:GetRepositoryPolicy",
                "ecr:DescribeRepositories",
                "ecr:ListImages",
                "ecr:DescribeImages",
                "ecr:BatchGetImage",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage"
            ],
          "Resource": "arn:aws:ecr:us-west-2:264318998405:apptoybox/today-tomorrow-api"
        }
    ]
}
```

5. Create the policy in AWS

```bash
aws iam create-policy  --policy-name GitHubActionsECRPushPolicy  --policy-document file://ecr-policy.json
```

6. Attach the policy to the role

```bash
aws iam attach-role-policy --role-name GitHubAction-AssumeRoleWithAction  --policy-arn arn:aws:iam::264318998405:policy/GitHubActionsECRPushPolicy
```

7. Confirm the policy is attached to the role

```bash
aws iam list-attached-role-policies --role-name GitHubAction-AssumeRoleWithAction
```
