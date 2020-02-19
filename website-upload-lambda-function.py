import json
import boto3
import io
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:988008946434:deployAEWebsiteTopic')

    location = {
       "bucketName": 'websitebuild.astropheenterprises.com',
       "objectKey": 'websitebuild.zip'
    }

    try:
        job = event.get("CodePipeline.job")

        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "BuildArtifact":
                    location = artifact["location"]["s3Location"]

        print ("Building website from" + str(location))

        s3 = boto3.resource('s3')

        website_bucket = s3.Bucket('website.astropheenterprises.com')
        websitebuild_bucket = s3.Bucket(location["bucketName"])

        website_zip = io.BytesIO()
        websitebuild_bucket.download_fileobj(location["objectKey"], website_zip)

        with zipfile.ZipFile(website_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                website_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')

        topic.publish(Subject="AEWebsite Published", Message="AE Website Updated")
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId = job["id"])

    except:
        topic.publish(Subject="AEWebsite Publish Failed", Message="AE Site Deploy Failed")
        raise

    return 'Hello from Lambda'
