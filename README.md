#  Arduino to AWS IoT Cloud Integration

This project connects an Arduino with AWS cloud services. It collects sensor data using Arduino and sends it to AWS IoT Core. From there, the data is processed using AWS Lambda and stored in S3. Logs can be viewed and monitored  in Cloud Watch. Cloud Watch Alarm is set for unusual behaviour.

#  AWS Services Used

- AWS IoT Core - receives data from Arduino.
- Dynamo db - used for real time monitoring.
- AWS Lambda - processes the data.
- Amazon S3 - stores the processed results for long time archival.
- Amazon CloudWatch - logs from Lambda function.
- AWS IAM - controls permissions securely.

#  Skills Demonstrated

- IoT + Cloud Integration
- Serverless architecture
- Real-time data processing
- AWS monitoring (CloudWatch)
- Cloud Watch alarms and SNS Notifications
- Secure AWS access with IAM