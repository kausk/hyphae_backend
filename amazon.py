import boto3

BUCKET_NAME = 'images-hyphae'


s3 = boto3.resource('s3')
location = boto3.client('s3').get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']


def upload_toS3(filename):
    result = s3.Bucket(BUCKET_NAME).upload_file(filename, filename, ExtraArgs={'ACL':'public-read'})
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, BUCKET_NAME, filename)
    return url

