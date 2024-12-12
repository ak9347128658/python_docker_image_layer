# Use the official AWS Lambda Python 3.8 runtime as the base image
FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
RUN pip install torch
# Copy the Lambda function code into the container
COPY app.py ${LAMBDA_TASK_ROOT}

# Command to run your function
CMD ["app.lambda_handler"]
