import boto3

aws_access_key = ''
aws_secret_key = ''
bucket_name = ''
file_key = ''


s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)


try:
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')


    print("File Contents:")
    print(content)

    value = int(content.strip())
    if value == 0:
        print("good")
    else:
        print("warning")

except Exception as e:
    print("Error reading file:", e)