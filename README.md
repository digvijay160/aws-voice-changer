# AWS Voice Changer

### Services Used

- AWS IAM : An IAM role for lambda function is created, and given full acces of below mentioned services.
- Amazon S3 Bucket : Stores input audio file, triggers lambda function on upload of file. Later stores, the final ouput audio file in different buckets.
- Amazon Transcribe : Converts the audio uploaded on S3 bucket to text.
- Amazon CloudWatch : It triggers the Lambda function when Transcribe completes its task.
- Amazon DynamoDB: Stores the text from Transcribe in a table.
- Amazon Polly : Converts the text received from Transcribe to a different voice.
- AWS Lambda : It takes the file from S3 to Transcribe, then text to Polly and DyanamoDB table, and the output file to S3 bucket.

```The code for lambda function is written in python```
