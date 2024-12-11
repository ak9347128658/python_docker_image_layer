import numpy as np

def lambda_handler(event, context):
    print("i am event:",event)
    if not event or 'numArray' not in event:
        return {
            'statusCode': 400,
            'body': 'Error: Missing "numArray" key in input'
        }
    
    # Use the numArray from the event
    num_array = event['numArray']
    arr = np.array(num_array)
    sum_arr = np.sum(arr)
    
    return {
        'statusCode': 200,
        'body': f"The sum of the array is: {sum_arr}"
    }
