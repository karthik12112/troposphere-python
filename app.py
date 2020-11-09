from flask import Flask
from flask import request
from flask import Response
import os
import time
import MySQLdb
import json
import boto3
import base64
from botocore.exceptions import ClientError

app = Flask(__name__)

session = boto3.session.Session()
client = session.client(
        service_name='secretsmanager',
        region_name="us-west-2"
    )

try:
    get_secret_value_response = client.get_secret_value(
        SecretId=os.environ['DB_Secret']
    )
except ClientError as e:
    if e.response['Error']['Code'] == 'DecryptionFailureException':
        # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'InternalServiceErrorException':
        # An error occurred on the server side.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'InvalidParameterException':
        # You provided an invalid value for a parameter.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'InvalidRequestException':
        # You provided a parameter value that is not valid for the current state of the resource.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
    elif e.response['Error']['Code'] == 'ResourceNotFoundException':
        # We can't find the resource that you asked for.
        # Deal with the exception here, and/or rethrow at your discretion.
        raise e
else:
    # Decrypts secret using the associated KMS CMK.
    # Depending on whether the secret is a string or binary, one of these fields will be populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
secret = json.loads(secret)


db  = MySQLdb.connect(os.environ['DB_Connection'], secret['username'], secret['password'])
MAIN_DB = db.cursor()


@app.route("/")
def hello():
    #curl -i http://$Server_IP:$Server_Port/
    return "<H1>Welcome to Python </H1>Checkpoint Date/Time: "+time.strftime("%c")+"\n"

@app.route("/health")
def health():
    return "Healthy"

@app.route("/init")
def init():
    #curl -i http://$Server_IP:$Server_Port/init
    MAIN_DB.execute("drop database if exists account")
    MAIN_DB.execute("create database account")
    MAIN_DB.execute("use account")
    sql = """create table users(
    ID int,
    USER varchar(20),
    DESCRIPTION varchar(250)
    )"""
    MAIN_DB.execute(sql)
    db.commit()
    return "## Database create new account table done ##\n"

@app.route("/users/insertuser", methods=['POST'])
def insertuser():
    req_json = request.get_json()
    #curl -i -H "Content-Type: application/json" -X POST -d '{"uid": "3", "user": "jimmy", "description": "security"}' $Server_IP:$Server_Port/users/insertuser
    sql = """insert into account.users(ID, USER, DESCRIPTION) values (%s, %s, %s)"""
    MAIN_DB.execute( sql, (req_json["uid"], req_json["user"], req_json["description"]) )
    db.commit()
    return Response(" ## record was added ## \n", status=200, mimetype='application/json')

@app.route("/users/<uid>")
def getuser(uid):
    #curl -i http://$Server_IP:$Server_Port/users/2
    MAIN_DB.execute("select user from account.users where id="+ str(uid))
    data = MAIN_DB.fetchone()
    if data:
        return (str(data[0])+"\n")
    else:
        return ("## not found ##")

@app.route("/users/removeuser/<uid>")
def deluser(uid):
    #curl -i http://$Server_IP:$Server_Port/users/removeuser/4
    MAIN_DB.execute("delete from account.users where id="+ str(uid))
    db.commit()
    return Response(" ## record was deleted ##\n", status=200, mimetype="application/json")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=True)
