import json

def lambda_handler(event, context):
    """
    Lambda function to handle chatbot requests
    """
    try:
        # Parse the request body
        body = json.loads(event['body'])
        user_message = body.get('message', 'Hello')
        
        # Simple echo response for now
        response_message = f"You said: {user_message}"
        
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST, OPTIONS"
            },
            'body': json.dumps({"response": response_message})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps({"error": str(e)})
        }
