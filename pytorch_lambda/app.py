import torch

def lambda_handler(event, context):
    # Check PyTorch version to ensure it's installed correctly
    body = event.get('body',"")
    print(f"Received body: {body}")
    print(f"PyTorch Version: {torch.__version__}")

    # Example: Simple tensor operation
    x = torch.rand(5, 3)
    print(x)

    return {
        'statusCode': 200,
        'body': "PyTorch is installed and working!"
    }

