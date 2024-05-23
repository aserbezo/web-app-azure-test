from django.shortcuts import render
from django.http import JsonResponse
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import os
import base64
import json

# Create your views here.

# Define the Cosmos endpoint and key
COSMOS_ENDPOINT=''
COSMOS_KEY= ''



# Initialize the Cosmos client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

# Define the database name
DATABASE_NAME = 'IoT'
database = client.get_database_client(DATABASE_NAME)
CONTAINER_NAME = 'devices'
container = database.get_container_client(CONTAINER_NAME)

query = "SELECT TOP 1 * FROM c ORDER BY c._ts DESC"

items = list(container.query_items(query=query, enable_cross_partition_query=True))


def get_latest_coordinates():
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)
    query = "SELECT TOP 1 * FROM c ORDER BY c._ts DESC"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if items:
        data = items[0]
        body = data['Body']
        decoded_bytes = base64.b64decode(body)
        decoded_str = decoded_bytes.decode('utf-8')
        result = json.loads(decoded_str)
        latitude = result['Latitude']
        longitude = result['Longitude']
        return {'latitude': latitude, 'longitude': longitude}
        print(latitude)
    return None


def latest_coordinates(request):
    coordinates = get_latest_coordinates()
    if coordinates:
        return JsonResponse(coordinates)
    return JsonResponse({'error': 'No data available'}, status=404)


def index(request):
    #context = get_latest_coordinates()
    return render(request, 'mapshow/map.html')