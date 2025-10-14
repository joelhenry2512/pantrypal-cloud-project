import json
import boto3
from datetime import datetime

# Initialize AWS clients
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# AWS Resources (replace with your actual values)
SNS_TOPIC_ARN = 'YOUR_SNS_TOPIC_ARN_HERE'  # Will be provided after topic creation
DYNAMODB_TABLE_NAME = 'ChatbotData'

def lambda_handler(event, context):
    """
    LF2 Lambda function that processes SQS messages
    - Reads messages from SQS
    - Queries DynamoDB for request details
    - Publishes results to SNS
    """
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Check if this is an SQS event
        if 'Records' not in event:
            print("No 'Records' found in event. This might not be an SQS trigger.")
            print(f"Event keys: {list(event.keys())}")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Invalid event format - no Records found',
                    'event_keys': list(event.keys())
                })
            }
        
        # Process each SQS record
        processed_count = 0
        for record in event['Records']:
            try:
                print(f"Processing record: {record.get('messageId', 'unknown')}")
                
                # Parse SQS message body
                if 'body' in record:
                    sqs_message = json.loads(record['body'])
                else:
                    print("No 'body' found in SQS record")
                    continue
                
                request_id = sqs_message.get('RequestID')
                session_id = sqs_message.get('SessionID')
                intent = sqs_message.get('Intent')
                product_type = sqs_message.get('ProductType', 'ingredients')
                location = sqs_message.get('Location', 'kitchen')
                
                print(f"Processing request {request_id} for intent {intent}")
                
                # Query DynamoDB for additional details
                try:
                    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
                    response = table.get_item(Key={'RequestID': request_id})
                    
                    if 'Item' in response:
                        db_item = response['Item']
                        print(f"Found DynamoDB record for {request_id}")
                        
                        # Update status to processed
                        table.update_item(
                            Key={'RequestID': request_id},
                            UpdateExpression='SET #status = :status, #processed_at = :processed_at',
                            ExpressionAttributeNames={
                                '#status': 'Status',
                                '#processed_at': 'ProcessedAt'
                            },
                            ExpressionAttributeValues={
                                ':status': 'Processed',
                                ':processed_at': datetime.utcnow().isoformat()
                            }
                        )
                        print(f"Updated DynamoDB record {request_id} to Processed")
                    else:
                        print(f"No DynamoDB record found for {request_id}")
                        
                except Exception as e:
                    print(f"Error querying DynamoDB: {str(e)}")
                
                # Generate processing result based on intent
                if intent == "GreetingIntent":
                    result_message = f"Hello! Your greeting has been processed. Request ID: {request_id}. I'm ready to help you with your culinary needs!"
                    
                elif intent == "ThankYouIntent":
                    result_message = f"Thank you for your appreciation! Request ID: {request_id}. I'm here to help you create amazing meals with your available ingredients."
                    
                elif intent == "ServiceRequestIntent":
                    result_message = f"Your cooking assistance request has been processed! Request ID: {request_id}. I can help you with {product_type} in your {location}. What specific ingredients do you have available?"
                    
                else:
                    result_message = f"Your request has been processed successfully. Request ID: {request_id}. I'm here to help with your culinary needs!"
                
                # Publish to SNS
                try:
                    if SNS_TOPIC_ARN == 'YOUR_SNS_TOPIC_ARN_HERE':
                        print("SNS_TOPIC_ARN not configured. Skipping SNS publish.")
                    else:
                        sns_response = sns.publish(
                            TopicArn=SNS_TOPIC_ARN,
                            Message=json.dumps({
                                'RequestID': request_id,
                                'SessionID': session_id,
                                'Intent': intent,
                                'ProductType': product_type,
                                'Location': location,
                                'ProcessedAt': datetime.utcnow().isoformat(),
                                'Message': result_message,
                                'Status': 'Processed'
                            }),
                            Subject=f'PantryPal Bot Response - Request {request_id}'
                        )
                        
                        print(f"Published to SNS: {sns_response['MessageId']}")
                        
                except Exception as e:
                    print(f"Error publishing to SNS: {str(e)}")
                    # Continue processing other records even if SNS fails
                
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing individual record: {str(e)}")
                continue
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully processed SQS messages',
                'processed_count': processed_count,
                'total_records': len(event['Records'])
            })
        }
        
    except Exception as e:
        print(f"Error in LF2 Lambda: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed to process SQS messages',
                'event_structure': list(event.keys()) if isinstance(event, dict) else str(type(event))
            })
        }
