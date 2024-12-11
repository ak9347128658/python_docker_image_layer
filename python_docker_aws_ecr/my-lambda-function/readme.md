# Deploying a Dockerized AWS Lambda Function with Numpy

To implement a Dockerfile for your AWS Lambda function that includes the numpy library, and to deploy it to AWS Elastic Container Registry (ECR), follow the steps below. The process will involve creating the Dockerfile, building the Docker image, pushing it to ECR, and then deploying it to AWS Lambda.

## Prerequisites

- AWS CLI configured with proper IAM permissions.
- Docker installed on your machine.
- AWS ECR repository created.
- AWS Lambda permissions for using ECR images.

## Step 1: Create Lambda Function with Numpy

Create a directory for your Lambda function.

```bash
mkdir my-lambda-function
cd my-lambda-function
```

Create a Python script (`lambda_function.py`) with the function code. Here’s a simple example that uses numpy.

```python
import numpy as np

def lambda_handler(event, context):
    # Example using numpy
    arr = np.array([1, 2, 3, 4])
    sum_arr = np.sum(arr)

    return {
        'statusCode': 200,
        'body': f"The sum of the array is: {sum_arr}"
    }
```

Create a `requirements.txt` file to list the dependencies. In this case, we need numpy.

```txt
numpy
```

## Step 2: Create the Dockerfile

Create a Dockerfile to containerize the Lambda function.

```Dockerfile
# Use the official AWS Lambda Python 3.8 base image
FROM public.ecr.aws/lambda/python:3.8

# Install dependencies
COPY requirements.txt  .
RUN pip install -r requirements.txt

# Copy the Lambda function code into the container
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (the entry point of the Lambda function)
CMD ["lambda_function.lambda_handler"]
```

## Step 3: Build and Test the Docker Image Locally

Build the Docker image:

In the directory where the Dockerfile and `lambda_function.py` are located, run the following command:

```bash
docker build -t my-lambda-image .
```

Run the Docker container locally to test if everything is working as expected:

```bash
docker run -p 9000:8080 my-lambda-image
```

Now, you can invoke the Lambda function locally by sending an HTTP request to the container:

```bash
Invoke-RestMethod -Method Post -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Body '{"numArray": [1, 2, 3, 4]}'
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
```

This should return a response similar to:

```json
{
  "statusCode": 200,
  "body": "The sum of the array is: 10"
}
```

## Step 4: Push the Docker Image to AWS ECR

Create an ECR repository:

If you don’t already have a repository, create one using the AWS CLI:

```bash
aws ecr create-repository --repository-name my-lambda-repo
```

Authenticate Docker to AWS ECR:

Run the following command to authenticate Docker to your ECR registry. Replace `aws_region` with your region.

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 851725421815.dkr.ecr.ap-south-1.amazonaws.com
```

Tag the Docker image to match the ECR repository name:

```bash
docker tag my-lambda-image:latest <aws_account_id>.dkr.ecr.aws_region.amazonaws.com/my-lambda-repo:latest
```

Push the Docker image to ECR:

Now push the Docker image to your ECR repository:

```bash
docker push <aws_account_id>.dkr.ecr.aws_region.amazonaws.com/my-lambda-repo:latest
```

## Step 5: Deploy the Docker Image to AWS Lambda

Create a Lambda function using the ECR image. You can do this via the AWS Management Console or the AWS CLI. Here’s the CLI command to create a Lambda function:

```bash
aws lambda create-function \
    --function-name my-lambda-function \
    --package-type Image \
    --code-image-uri <aws_account_id>.dkr.ecr.aws_region.amazonaws.com/my-lambda-repo:latest \
    --role arn:aws:iam::<aws_account_id>:role/service-role/<lambda-execution-role>
```

Replace the following placeholders:

- `<aws_account_id>` with your AWS account ID.
- `<aws_region>` with your region.
- `<lambda-execution-role>` with the ARN of the IAM role that has Lambda execution permissions.

Test the Lambda function:

Once the function is created, you can invoke it using the AWS CLI:

```bash
aws lambda invoke --function-name my-lambda-function output.txt
```

This will store the response in `output.txt`. You should see the sum of the array as the result.

## Step 6: Clean up (optional)

If you no longer need the Lambda function or the ECR repository, you can delete them to avoid further charges:

Delete the Lambda function:

```bash
aws lambda delete-function --function-name my-lambda-function
```

Delete the ECR repository:

```bash
aws ecr delete-repository --repository-name my-lambda-repo --force
```

## Summary

- Created a Python Lambda function with the numpy library.
- Created a Dockerfile to containerize the Lambda function.
- Built the Docker image and tested it locally.
- Pushed the Docker image to AWS ECR.
- Deployed the Docker image to AWS Lambda.

By following these steps, you'll be able to use a custom Docker image for your AWS Lambda function, including the numpy library or any other dependencies you require.
