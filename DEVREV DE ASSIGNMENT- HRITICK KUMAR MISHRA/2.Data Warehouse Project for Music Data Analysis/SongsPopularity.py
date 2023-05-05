#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import configparser
import psycopg2
import boto3

# Read config file
config = configparser.ConfigParser()
config.read('dwh.cfg')

# Set credentials for Redshift cluster
redshift_host = config.get("CLUSTER", "HOST")
redshift_port = config.get("CLUSTER", "DB_PORT")
redshift_db = config.get("CLUSTER", "DB_NAME")
redshift_user = config.get("CLUSTER", "DB_USER")
redshift_password = config.get("CLUSTER", "DB_PASSWORD")

# Connect to Redshift cluster
conn = psycopg2.connect(f"host={redshift_host} port={redshift_port} dbname={redshift_db} user={redshift_user} password={redshift_password}")
cur = conn.cursor()

# Create staging tables in Redshift
cur.execute("""CREATE TABLE IF NOT EXISTS staging_events (
                artist TEXT,
                auth TEXT,
                firstName TEXT,
                gender TEXT,
                itemInSession INT,
                lastName TEXT,
                length FLOAT,
                level TEXT,
                location TEXT,
                method TEXT,
                page TEXT,
                registration FLOAT,
                sessionId INT,
                song TEXT,
                status INT,
                ts BIGINT,
                userAgent TEXT,
                userId INT);
            """)

cur.execute("""CREATE TABLE IF NOT EXISTS staging_songs (
                num_songs INT,
                artist_id TEXT,
                artist_latitude FLOAT,
                artist_longitude FLOAT,
                artist_location TEXT,
                artist_name TEXT,
                song_id TEXT,
                title TEXT,
                duration FLOAT,
                year INT);
            """)

# Load log data from S3 bucket into staging_events table
s3 = boto3.client('s3',
                  region_name=config.get('AWS', 'REGION'),
                  aws_access_key_id=config.get('AWS', 'ACCESS_KEY'),
                  aws_secret_access_key=config.get('AWS', 'SECRET_KEY')
                  )

log_data_path = f"s3://{config.get('S3', 'LOG_DATA')}"
s3_copy_command = f"""COPY staging_events FROM '{log_data_path}' CREDENTIALS 'aws_iam_role={config.get('IAM_ROLE', 'ARN')}' FORMAT as json '{config.get('S3', 'LOG_JSONPATH')}'"""
cur.execute(s3_copy_command)

# Load song data from S3 bucket into staging_songs table
song_data_path = f"s3://{config.get('S3', 'SONG_DATA')}"
s3_copy_command = f"""COPY staging_songs FROM '{song_data_path}' CREDENTIALS 'aws_iam_role={config.get('IAM_ROLE', 'ARN')}' FORMAT as json 'auto'"""
cur.execute(s3_copy_command)

# Close connection to Redshift cluster
conn.commit()
conn.close()

