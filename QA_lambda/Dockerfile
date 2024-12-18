# Use the official AWS Lambda Python 3.9 base image
FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
RUN pip install --no-cache-dir \
    pdfplumber \
    pymongo \
    boto3 \
    torch==1.12.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html \
    requests \
    groq \
    numpy

# Copy the Lambda function code into the container
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (the entry point of the Lambda function)
CMD ["lambda_function.lambda_handler"]
