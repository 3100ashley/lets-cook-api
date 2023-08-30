from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import boto3 
@api_view(['GET', 'POST'])
def recipes(request):
      db =  boto3.resource('dynamodb')
      table = db.Table('recipes')
      if request.method == 'GET':
        recipes = table.scan()
        return Response({"recipes": recipes.get('Items')})
      elif request.method == 'POST':
          try:  
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_201_CREATED)
          except:
              return Response({'error': 'Failed to insert'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET','PUT', 'DELETE'])         
def recipe(request,id):
    db =  boto3.resource('dynamodb')
    table = db.Table('recipes')
    if request.method == 'GET':
        recipe = table.get_item(Key={
            'id':id
        })
        if recipe.get('Item') is not None:
            return Response({'recipe': recipe.get('Item')})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        try:  
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Failed to update'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if request.method == 'DELETE':
        table.delete_item(Key={'id':id})
        return Response(status=status.HTTP_200_OK)