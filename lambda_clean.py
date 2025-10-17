import json

def lambda_handler(event, context):
    """
    Clean Lambda function for PantryPal chatbot
    """
    print("Received event:", json.dumps(event))
    
    try:
        # Parse the request body
        if 'body' in event:
            body = json.loads(event['body'])
            user_message = body.get('message', 'Hello')
        else:
            user_message = 'Hello'
        
        print(f"User message: {user_message}")
        
        # Simple response logic
        if 'hello' in user_message.lower():
            response_text = f"Hello! I'm PantryPal. You said: {user_message}. What ingredients do you have today?"
        elif 'thank' in user_message.lower():
            response_text = f"You're welcome! You said: {user_message}. I'm here to help with your cooking needs!"
        elif 'cook' in user_message.lower() or 'ingredient' in user_message.lower():
            response_text = f"Great! You said: {user_message}. I can help you find recipes with your available ingredients!"
        else:
            response_text = f"You said: {user_message}. I'm PantryPal, your culinary assistant. How can I help you cook today?"
        
        # Return response
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'response': response_text
            })
        }
        
        print("Returning response:", response)
        return response
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
