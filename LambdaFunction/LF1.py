#aws lambda code for 
#How to Make a Chatbot Using Amazon Lex and AWS Lambda (Python) | Conversational AI Part 2
# https://youtu.be/W6T-RFei6SY
import json
import datetime
import time
import boto3
import logging



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
SQS = boto3.client("sqs")

""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """

# def getQueueURL():
#     """Retrieve the URL for the configured queue name"""
#     q = SQS.get_queue_url(QueueName='DiningConciergeSQS').get('QueueUrl')
#     return q
    
def record(event):
    """The lambda handler"""
    logger.debug("Recording with event %s", event)
    data = event.get('data')
    try:
        logger.debug("Recording %s", data)
        #u = getQueueURL()
        u='https://sqs.us-east-1.amazonaws.com/637423430782/dccSQS'
        logging.debug("Got queue URL %s", u)
        resp = SQS.send_message(
            QueueUrl=u, 
            MessageBody="Dining Concierge message from LF1 ",
            MessageAttributes={
                "Location": {
                    "StringValue": str(get_slots(event)["LocationSlot"]),
                    "DataType": "String"
                },
                "Cuisine": {
                    "StringValue": str(get_slots(event)["CuisineType"]),
                    "DataType": "String"
                },
                "PeopleCount" : {
                    "StringValue": str(get_slots(event)["People"]),
                    "DataType": "String"
                },
                "Date" : {
                    "StringValue": get_slots(event)["Date"],
                    "DataType": "String"
                },
                "PhoneNumber" : {
                    "StringValue": str(get_slots(event)["PhoneNumber"]),
                    "DataType": "String"
                }
            }
        )
        logger.debug("Send result: %s", resp)
    except Exception as e:
        raise Exception("Could not record link! %s" % e)



def get_slots(intent_request):
    return intent_request['intent']['slots']
    
def validate(slots):

    valid_cities = ['mumbai','delhi','banglore','hyderabad']
    
    if not slots['LocationSlot']:
        print("Inside Empty Location")
        return {
        'isValid': False,
        'violatedSlot': 'LocationSlot'
        }        
        
    if slots['LocationSlot']['value']['originalValue'].lower() not in  valid_cities:
        
        print("Not Valide location")
        
        return {
        'isValid': False,
        'violatedSlot': 'LocationSlot',
        'message': 'We currently  support only {} as a valid destination.?'.format(", ".join(valid_cities))
        }
        
    if not slots['CuisineType']:
        
        return {
        'isValid': False,
        'violatedSlot': 'CuisineType',
    }
        
    if not slots['People']:
        return {
        'isValid': False,
        'violatedSlot': 'People'
    }
        
    if not slots['Date']:
        return {
        'isValid': False,
        'violatedSlot': 'Date'
    }

    if not slots['PhoneNumber']:
        return {
        'isValid': False,
        'violatedSlot': 'PhoneNumber'
    }
    
    return {'isValid': True}
    
def lambda_handler(event, context):
    
    # print(event)
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            
            if 'message' in validation_result:
            
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": validation_result['message']
                    }
                ]
               } 
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                }
               } 
    
            return response
           
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name':intent,
                    'slots': slots
                    
                    }
        
            }
        }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        # Add order in Database
        
        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                }
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Thanks, I have placed your reservation"
            }
        ]
    }
            
        return response