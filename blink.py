import boto3
import RPi.GPIO as GPIO
import time

# AWS S3 credentials and file information
aws_access_key = ''
aws_secret_key = ''
bucket_name = ''
file_key = ''

# Initialize AWS S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Initialize GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)  # LED connected to pin 20 (BCM)
GPIO.setup(21, GPIO.OUT)  # LED connected to pin 21 (BCM)

p20 = GPIO.PWM(20, 50)  # Create PWM object for pin 20
p21 = GPIO.PWM(21, 50)  # Create PWM object for pin 21

# Turn off both LEDs before turning on the selected one
p20.stop()
p21.stop()

try:
    # Read the content from the file once
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')
    value = int(content.strip())
    
    # Process based on the read value
    if value == 0:
        print("File Contents:", content)
        print("good")
        p20.start(0)
        for _ in range(5):  # Repeat the loop 5 times
            for dc in range(0, 101, 5):
                p20.ChangeDutyCycle(dc)
                time.sleep(0.05)
            for dc in range(100, -1, -5):
                p20.ChangeDutyCycle(dc)
                time.sleep(0.05)
        p20.stop()  # Stop the LED after 5 repetitions
    elif value == 1:
        print("File Contents:", content)
        print("warning")
        p21.start(0)
        for _ in range(5):  # Repeat the loop 5 times
            for dc in range(0, 101, 5):
                p21.ChangeDutyCycle(dc)
                time.sleep(0.05)
            for dc in range(100, -1, -5):
                p21.ChangeDutyCycle(dc)
                time.sleep(0.05)
        p21.stop()  # Stop the LED after 5 repetitions
    else:
        print("Invalid value")
            
except Exception as e:
    print("Error reading file:", e)

except KeyboardInterrupt:
    pass

# Cleanup GPIO
GPIO.cleanup()