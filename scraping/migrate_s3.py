import boto3
import os
from tqdm import tqdm

to_upload = os.listdir('pages')
s3 = boto3.resource('s3')
for i in tqdm(to_upload):
    s3.meta.client.upload_file('pages/'+i, 'minecraft-qa-2019', i)