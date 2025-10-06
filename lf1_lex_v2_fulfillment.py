import json
import boto3

def lambda_handler(event, context):
    """
    LF1 Lambda function for Lex V2 bot fulfillment
    Handles different intents and provides appropriate responses
    """
    try:
        # Extract the intent name from the Lex V2 event
        intent = event['sessionState']['intent']['name']
        
        # Handle different intents
        if intent == "GreetingIntent":
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
                        "content": "Hello! I'm PantryPal, your culinary assistant. What ingredients do you have today?"
                    }
                ]
            }
        
        elif intent == "ThankYouIntent":
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
                        "content": "You're welcome! I'm here to help you create amazing meals. What ingredients would you like to work with?"
                    }
                ]
            }
        
        elif intent == "ServiceRequestIntent":
            # Extract slots if they exist
            slots = event['sessionState']['intent'].get('slots', {})
            product_type = slots.get('ProductType', {}).get('value', {}).get('interpretedValue', 'ingredients')
            location = slots.get('Location', {}).get('value', {}).get('interpretedValue', 'your kitchen')
            
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
                        "content": f"Great! I can help you with {product_type} in {location}. What specific ingredients do you have available? I'll suggest some delicious recipes!"
                    }
                ]
            }
        
        else:
            # Default response for unknown intents
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
                        "content": "I'm here to help you with your culinary needs! What ingredients do you have today?"
                    }
                ]
            }
    
    except Exception as e:
        # Error handling
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
