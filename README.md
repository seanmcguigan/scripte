# Backsup to s3

Define vars in src/gunzip_to_s3.py source_dir(what you want to backup), backup_dir(local backup, retained for 7 days), bucketname(The name of the s3 bucket).

Compressed backups will be created within its corrosponding key. Key format 'Year-Month'

'''
2018-10
├── JenkinsMaster_2018-10-04_16:23:28.tar.gz
├── JenkinsMaster_2018-10-04_16:23:57.tar.gz
└── JenkinsMaster_2018-10-04_16:24:58.tar.gz
'''

