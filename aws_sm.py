#!/usr/bin/env python3

import boto3

from os import listdir
from os.path import isfile, join

profile = input("Enter AWS profile: ")

boto3.setup_default_session(profile_name=profile)

client = boto3.client('secretsmanager', region_name="eu-central-1")

#Variables
env = "stage"
account_id = "0000000000"
region = "eu-central-1"
costcenter = "stage-costcenter"

Name = "stage/ssh-key/"

mypath = input("Please enter path to keys: ")

#Get files name from directiry
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#Create secrets
for i in onlyfiles:
    f = open(mypath + "/" + i, 'r')
    response = client.create_secret(
        Name=Name + i,
        SecretString=f.read(),
        Description='Key for ' + Name + i + ' created by Python',
        Tags=[
            {
                'Key': 'Name', 
                'Value': Name + i
            },
            {
                'Key': 'owner', 
                'Value': 'ITOps'
            },
            {
                'Key': 'costcenter', 
                'Value': costcenter
            },
            {
                'Key': 'aws_stage_account_id', 
                'Value': account_id
            },
            {
                'Key': 'aws_environment', 
                'Value': env
            },
            {
                'Key': 'region', 
                'Value': region
            },
            {
                'Key': 'Description', 
                'Value': 'Managed by Python script'
            },
        ]
    )
    continue