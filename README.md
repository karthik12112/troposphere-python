# troposphere

Python module to build CloudFormation Template for reusability of code

# Application Deployment

cd fargate

sh wraper.sh -r us-west-2

After build is successful login into AWS << Codebuild << DevopsBuild

##artifacts

All are stored in s3://kanna-karthik-interview

##Update environment variables for codebuild

developerfilename - name of developer file - Eg: sample-app.tgz

path - where metadata.yaml is available - Eg: metadata/metadata.yaml

## What developer needs to do to his app

mkdir metadata

create metadata as in [metadata](fargate/sampleapp/metadata/metadata.yaml)

dockerfile should not be inside some directory

tar -zcvf sample-app.tgz .

```
tar -zcvf sample-app.tgz .
aws s3 cp sample-app.tgz s3://kanna-karthik-interview/

```

# Sample App

- Python Flask
- Mysql

# AWS services

- RDS - Mysql
- SSM - Secret Manager
- EC2 - ALB
- VPC
- ECS - Fargate
- IAM
- CloudWatch

# Deploying Application

## Network
To deploy network, create yaml file as
[metadata](network/metadata/293393888753.yaml)

> cd network && python3 build_network.py --path metadata/293393888753.yaml --region "us-west-2"

It does not deploy network but builds cloudformation template in
fargate/build_fargate.yaml

## APP
To deploy APP, developers needs to create yaml file as
[metadata](fargate/sampleapp/metadata/metadata.yaml) and Dockerfile in their repo

Generate Access and Secret key


> cd fargate && python3 deploy_fargate.py --account 293393888753 --region "us-west-2" --path "./metadata/test_service.yaml" --stack_name "base-stack"

## Validating App

Loadbalancer Ports:

$Server_Port - Blue - 80 and green - 8080

Loadbalancer URL
[http://$Server_IP](http://base-st-ALB-1LJIKWGM0PPMN-50054144.us-west-2.elb.amazonaws.com) - Output from  CloudFormation Stack base-stack

Home page - Welcome Screen
`curl -i http://$Server_IP:$Server_Port/`

Creates new account table in Databse
`curl -i http://$Server_IP:$Server_Port/init`

Adding records to table
`curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "3", "user": "jimmy", "description": "security"}' $Server_IP:$Server_Port/users/insertuser`

Get user details
`curl -i http://$Server_IP:$Server_Port/users/2`

To delete a record from database
`curl -i http://$Server_IP:$Server_Port/users/removeuser/4`


# Cloudformation Stacks

NetworkStack - Builds complete network in AWS

BaseStack - Developers Stack - name depends on developer

devopsstack - For devops team to migrate applications to fargate blue green


#what needs to be done!

######Network:

- Support multiple ip's to whitelist at security Group
- Enable VPC flowlogs
- Serverless to deploy network using api gateway
- Endpoints for secure communication
- Create a deployment stack instead of manual deployment
- Add support to peering/transit gateway


######Fargate:

- Autoselect subnets if not specified
- cmk for secretsmanager
- convert into libs for code reusability
- minimum iam permissions
- wrapper to deploy stacks
- role name should be service name

######Deploystack:

- codepipeline/codedeploy for application Deployment
- And few more changes
