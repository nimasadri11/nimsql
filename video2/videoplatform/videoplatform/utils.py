from .models import *
import boto3
from botocore.exceptions import ClientError
from .models import *

def get_videos(n=-1, sort_by="-uploadtime"):
    videos = Video.objects.all().order_by(sort_by)
    # videos = []
    if n >= 0:
        videos = videos[:n]
    return videos
    
def get_url(s):
    return s.replace(" ", "-")

def upload_s3(f, key):
    # pass
    s3_client = boto3.client('s3')
    client = boto3.client('s3')
    client.put_object(Body=f, Bucket='kyt-vibin', Key=key, ACL='public-read')
    
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)

def get_creators():
    return Creator.objects.all()
