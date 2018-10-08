#!/usr/bin/env python

# tars a local dir and backsup to s3

import os
import tarfile
import shutil  
from datetime import datetime, date, time, timedelta
import boto3
from glob import glob

now        = datetime.now()
last_week  = 'JenkinsMaster_%s' % datetime.strftime(datetime.now() - timedelta(7), "%Y-%m-%d")
tarball    = 'JenkinsMaster_%s.tar.gz' % now.strftime("%Y-%m-%d_%H%M%S")
source_dir = '/var/log/'
backup_dir = '../backups/'
s3         = boto3.client('s3')
bucketname = "efs-tar-target"
key        = now.strftime("%Y-%m")

# tar the directory
def make_tarfile(output_filename, source_dir):
    try :
        with tarfile.open(output_filename, "w:gz", compresslevel = 9) as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            shutil.move(tarball, backup_dir)
            os.chdir(backup_dir)
    except:
      print ('Something failed while creating archive of directory {0}'.format(source_dir))
      raise

# deploy to s3
def deploy():
    try:
      s3.upload_file(Filename=tarball,Bucket=bucketname,Key=key + '/' + tarball)
    except NameError:
      print('Something failed while uploading %s' % tarball)
      raise

# remove local backups older that 7 days
def cleanup():
  try:
    for filename in glob(backup_dir+"/"+last_week+"*"):
      os.remove(os.path.basename(filename))
  except:
    print('Something failed while removing %s' % tarball)
    raise

if __name__ == '__main__':
    make_tarfile(tarball, source_dir)

response    = s3.list_objects_v2(Bucket=bucketname,MaxKeys=1,Prefix=key + '/')
file_exists = response['KeyCount']
upload      = "Uploading %s to s3 Bucket %s" % (tarball,bucketname + '/' + key)
key_upload  = "Creating key: %s - uploading %s to s3 Bucket %s" % (key,tarball,bucketname + '/' + key)
reply       = upload if file_exists else key_upload

print(reply)

if __name__ == '__main__':
    deploy()
    cleanup()
