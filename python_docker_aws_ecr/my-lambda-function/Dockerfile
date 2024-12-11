# Use the official AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
COPY requirements.txt  .
RUN pip install -r requirements.txt

# Copy the Lambda function code into the container
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (the entry point of the Lambda function)
CMD ["lambda_function.lambda_handler"]