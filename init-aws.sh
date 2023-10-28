#!/bin/bash
awslocal s3 mb s3://clientbucket4321
awslocal s3 mb s3://serverbucket4321
awslocal sqs create-queue --queue-name my-queue --region eu-central-1
