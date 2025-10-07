import json
import boto3
import uuid
from datetime import datetime

# Initialize AWS clients
sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')

# AWS Resources (replace with your actual values)
SQS_QUEUE_URL = 'YOUR_SQS_QUEUE_URL_HERE'  # Will be provided after queue creation
DYNAMODB_TABLE_NAME = 'ChatbotData'

def lambda_handler(event, context):
    """
    Enhanced LF1 Lambda function for Lex V2 bot fulfillment
    Integrates with SQS for message queuing and DynamoDB for data storage
    """
    try:
        # Extract information from the Lex V2 event
        session_id = event.get('sessionId', 'unknown')
        intent = event['sessionState']['intent']['name']
        slots = event['sessionState']['intent'].get('slots', {})
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Extract slot values
        product_type = slots.get('ProductType', {}).get('value', {}).get('interpretedValue', 'ingredients')
        location = slots.get('Location', {}).get('value', {}).get('interpretedValue', 'kitchen')
        
        # Create request data for storage
        request_data = {
            'RequestID': request_id,
            'SessionID': session_id,
            'Intent': intent,
            'ProductType': product_type,
            'Location': location,
            'Timestamp': datetime.utcnow().isoformat(),
            'Status': 'Processing'
        }
        
        # Store in DynamoDB
        try:
            table = dynamodb.Table(DYNAMODB_TABLE_NAME)
            table.put_item(Item=request_data)
            print(f"Stored request {request_id} in DynamoDB")
        except Exception as e:
            print(f"Error storing in DynamoDB: {str(e)}")
        
        # Send message to SQS for processing
        try:
            sqs_message = {
                'RequestID': request_id,
                'SessionID': session_id,
                'Intent': intent,
                'ProductType': product_type,
                'Location': location,
                'Timestamp': datetime.utcnow().isoformat()
            }
            
            sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(sqs_message)
            )
            print(f"Sent message {request_id} to SQS")
        except Exception as e:
            print(f"Error sending to SQS: {str(e)}")
        
        # Handle different intents with enhanced responses
        if intent == "GreetingIntent":
            response_message = f"Hello! I'm PantryPal, your culinary assistant. I've logged your greeting (Request ID: {request_id}). What ingredients do you have today?"
            
        elif intent == "ThankYouIntent":
            response_message = f"You're welcome! I'm here to help you create amazing meals. Your thanks have been recorded (Request ID: {request_id}). What ingredients would you like to work with?"
            
        elif intent == "ServiceRequestIntent":
            response_message = f"Great! I can help you with {product_type} in {location}. Your request has been queued for processing (Request ID: {request_id}). What specific ingredients do you have available? I'll suggest some delicious recipes!"
            
        else:
            response_message = f"I'm here to help you with your culinary needs! Your request has been logged (Request ID: {request_id}). What ingredients do you have today?"
        
        # Return Lex V2 response format
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": response_message
                }
            ]
        }
    
    except Exception as e:
        # Error handling
        print(f"Error in Lambda function: {str(e)}")
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": "Error",
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Sorry, I encountered an error. Please try again!"
                }
            ]
        }
