from flask import Flask,request
from flask_restful import Resource, Api
import boto3

app = Flask(__name__)
api = Api(app)


'''
Service for fantasy player data
'''
class Fantasy_Players(Resource):
    '''
    Example POST request:
    {
        "name":"john-doe",
        "year":2019,
        "division":"West",
        "team":{'QB':"Russell Willson", "RB" : "Marshawn Lynch"}
    }
    '''
    def post(self):
        #Skip Content type requirement
        event = request.get_json(force=True)
        #Check for correct data
        required = ['name','year','division','team']
        given = list(event.keys())
        #If required data is not found
        if (not all(item in given for item in required)):
            return {"body":"Bad Request!"},400
        
        #Init dynamo Client
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
        table = dynamodb.Table('NflPlayers')
        try:
            response = table.put_item(
                Item = {
                    'name':event['name'],
                    'year':event['year'],
                    'division':event['division'],
                    'team':event['team']

                }
            )
        except ClientError as e:
            return{
                'body':"Error Creating"
            },502
        return {
            "body":"Successful Creation"
        },201


    '''
    Needs header element of name.
    Example: apicall/fantasy_players?name=name-of-player
    '''
    def get(self):
        name  = request.headers.get('name')
        #Bad request if there is no name header. 
        if(name == None):
            return {'body':'Bad Request!'},400
        #Init and query Dynamo Table
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        table = dynamodb.Table('FantasyPlayers')
        try:
            response = table.query(
                KeyConditionExpression = Key('name').eq(name)
            )
        except ClientError as e:
            return{
                'body':"Error Querying"
            },502
        return response['Items'],200
    
    '''
        Takes in identical JSON input as POST method
    '''
    def put(self):
        #Skip Content type requirement
        event = request.get_json(force=True)    
        #Check for correct data
        required = ['name','year','division','team']
        given = list(event.keys())
        #If required data is not found
        if (not all(item in given for item in required)):
            return {"body":"Bad Request!"},400    
        #Init dynamo
        dynamodb = boto3.resource("dynamodb",region_name = 'us-east-1')
        table = dynamodb.Table('FantasyPlayers')
        try:
            response = table.update_item(
                Key = {
                    'User':pk
                },
                #Tell dynamo to update based on new values
                UpdateExpression = "set name = :n, year =:y, division =:d ,team =:t",
                ExpressionAttributeValues={
                    ':n':event['name'],
                    ':y':event['year'],
                    ':d':event['division'],
                    ':t':event['team']
                    
                }
            )
        except ClientError as e:
            return{
                'body':"Error Updating"
            },502

        return{
            'body':'Successful Update'
        },200
    
    '''
    Needs header element of name.
    Example: apicall/fantasy_players?name=name-of-player
    '''
    def delete(self):
        name  = request.headers.get('name')
        #Bad request if there is no name header. 
        if(name == None):
            return {'body':'Bad Request!'},400
        #Init and query Dynamo Table
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        table = dynamodb.Table('FantasyPlayers')
        
        try:
            response = table.delete_item(
                Key = {
                    'name' : name
                }    
            )
        except ClientError as e:
            return{
                'body':"Error Deleting"
            },502
        
        return {
            'body':'Successful Deletion'
        },200
'''
Service for NFL player fantasy data
'''
class Nfl_Players(Resource):
    '''
    Example POST request:
    {
        "name":"Drew Brees",
        "position":"QB",
        "team":"Saints",
        "points":{2018:{'@ATL':43.2, 'CAR' : 20.1},2019{....}}
    }
    '''
    def post(self):
        #Skip Content type requirement
        event = request.get_json(force=True)
        #Check for correct data
        required = ['name','position','points','team']
        given = list(event.keys())
        #If required data is not found
        if (not all(item in given for item in required)):
            return {"body":"Bad Request!"},400
        
        #Init dynamo Client
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
        table = dynamodb.Table('NflPlayers')
        try:
            response = table.put_item(
                Item = {
                    'name':event['name'],
                    'points':event['points'],
                    'position':event['position'],
                    'team':event['team']

                }
            )
        except ClientError as e:
            return{
                'body':"Error Creating"
            },502
        return {
            "body":"Successful Creation"
        },201


    '''
    Needs header element of name.
    Example: apicall/nfl_players?name=name-of-player
    '''
    def get(self):
        name  = request.headers.get('name')
        #Bad request if there is no name header. 
        if(name == None):
            return {'body':'Bad Request!'},400
        #Init and query Dynamo Table
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        table = dynamodb.Table('NflPlayers')
        try:
            response = table.query(
                KeyConditionExpression = Key('name').eq(name)
            )
        except ClientError as e:
            return{
                'body':"Error Querying"
            },502
        return response['Items'],200
    
    '''
        Takes in identical JSON input as POST method
    '''
    def put(self):
        #Skip Content type requirement
        event = request.get_json(force=True)    
        #Check for correct data
        required = ['name','position','points','team']
        given = list(event.keys())
        #If required data is not found
        if (not all(item in given for item in required)):
            return {"body":"Bad Request!"},400    
        #Init dynamo
        dynamodb = boto3.resource("dynamodb",region_name = 'us-east-1')
        table = dynamodb.Table('NflPlayers')
        try:
            response = table.update_item(
                Key = {
                    'User':pk
                },
                #Tell dynamo to update based on new values
                UpdateExpression = "set name = :n, position =:p, points =:po ,team =:t",
                ExpressionAttributeValues={
                    ':n':event['name'],
                    ':p':event['position'],
                    ':po':event['points'],
                    ':t':event['team']
                    
                }
            )
        except ClientError as e:
            return{
                'body':"Error Updating"
            },502

        return{
            'body':'Successful Update'
        },200
    
    '''
    Needs header element of name.
    Example: apicall/nfl_players?name=name-of-player
    '''
    def delete(self):
        name  = request.headers.get('name')
        #Bad request if there is no name header. 
        if(name == None):
            return {'body':'Bad Request!'},400
        #Init and query Dynamo Table
        dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
        table = dynamodb.Table('NflPlayers')
        
        try:
            response = table.delete_item(
                Key = {
                    'name' : name
                }    
            )
        except ClientError as e:
            return{
                'body':"Error Deleting"
            },502
        
        return {
            'body':'Successful Deletion'
        },200

'''
Set host open to all ports. This allows the API to be accessed from all ports within a Docker 
container
'''
api.add_resource(Fantasy_Players,'/fantasy_players')
api.add_resource(Nfl_Players,'/nfl_players')

if __name__ == '__main__':
    app.run(host='0.0.0.0')