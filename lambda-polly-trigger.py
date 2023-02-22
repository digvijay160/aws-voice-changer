import re
import json
import boto3
import os
import uuid
import urllib.request
from contextlib import closing

s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe')
#dynamodb = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    
    recordId = str(uuid.uuid4())
    
    #get the Transcribe job # and result
    job_name = event['detail']['TranscriptionJobName']
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(uri)
    
    content = urllib.request.urlopen(uri).read().decode('UTF-8')
    #write content to cloudwatch logs
    print(json.dumps(content))
    
    #get text from Transcribe
    data =  json.loads(content)
    transcribed_text = data['results']['transcripts'][0]['transcript']
    print(transcribed_text)
    
    #Call Polly to do Text-to-speech
    voiceId = 'Joanna' # You can change this, or get input as a variable

    polly = boto3.client('polly')
    response = polly.synthesize_speech(
        OutputFormat='mp3',
        Text = transcribed_text,
        VoiceId = voiceId
        )
        
    #Output to the S3 bucket    
    BUCKET_NAME = "voice-chan-ouput"
    s3 = boto3.client('s3')
    s3.put_object(
        Body = response['AudioStream'].read(),
        Bucket=BUCKET_NAME, 
        Key= "newvoice.mp3")
        
    #Add the text to the DynamoDB table
    recordId = str(uuid.uuid4())
    
    print('Generating new DynamoDB record, with ID: ' + recordId)
    print('Input Text: ' + transcribed_text)
    print('Selected voice: ' + voiceId)
    
    #Creating new record in DynamoDB table
    table = dynamodb.Table('voice-changer-dynamoDB')
    data = table.put_item(
        Item={
            "id" : recordId,
            "text" : transcribed_text,
            "voice" : voiceId
        }
    )

    response = {
        'statusCode': 200,
        'body': 'successfully created item!',
        'headers': {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
    }
  
    return response 