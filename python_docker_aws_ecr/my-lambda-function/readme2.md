## Step 1: Create an ECR Repository Using the AWS Management Console

### Login to AWS Management Console

Go to AWS Management Console and log in.

### Navigate to ECR

In the AWS Management Console, search for "ECR" in the search bar and select Elastic Container Registry.

### Create a New Repository

1. In the left-hand sidebar, click on **Repositories**.
2. Click the **Create repository** button.

### Configure Repository Settings

- **Repository name**: Enter a name for your repository (e.g., `my-lambda-repo`).

## Step 2: Push the Docker Image to the Newly Created ECR Repository

### Authenticate Docker to ECR

In the AWS ECR Console, under your repository, find the **View push commands** section. Copy and run the command to authenticate Docker to your ECR registry:

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 851725421815.dkr.ecr.ap-south-1.amazonaws.com
```

### Tag your Docker image

Replace `<aws-account-id>` with your account ID and `<aws-region>` with your region:

```bash
docker tag my-lambda-image:latest 851725421815.dkr.ecr.ap-south-1.amazonaws.com/my-lambda-repo:latest
```

### Push the image to ECR

```bash
docker push 851725421815.dkr.ecr.ap-south-1.amazonaws.com/my-lambda-repo:latest
```

## Step 3: Create the Lambda Function Using the ECR Image

Create the Lambda function using the container image.
