from azure.cosmos import CosmosClient, exceptions
import os
import uuid
from datetime import datetime

# Initialize Cosmos DB client
COSMOS_ENDPOINT = os.getenv('COSMOS_ENDPOINT')
COSMOS_KEY = os.getenv('COSMOS_KEY')
DATABASE_NAME = 'synapsee_db'
USERS_CONTAINER = 'users'
REPORTS_CONTAINER = 'reports'

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
users_container = database.get_container_client(USERS_CONTAINER)
reports_container = database.get_container_client(REPORTS_CONTAINER)

def create_user(username, email, hashed_password):
    user = {
        'id': str(uuid.uuid4()),
        'username': username,
        'email': email,
        'password': hashed_password,
        'created_at': datetime.utcnow().isoformat()
    }
    users_container.create_item(user)
    return user

def get_user_by_username(username):
    query = f"SELECT * FROM c WHERE c.username = '{username}'"
    items = list(users_container.query_items(query, enable_cross_partition_query=True))
    return items[0] if items else None

def save_report(user_id, product_data, analysis_results, pdf_url):
    report = {
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'product_data': product_data,
        'analysis_results': analysis_results,
        'pdf_url': pdf_url,
        'created_at': datetime.utcnow().isoformat()
    }
    reports_container.create_item(report)
    return report

def get_user_reports(user_id):
    query = f"SELECT * FROM c WHERE c.user_id = '{user_id}' ORDER BY c.created_at DESC"
    return list(reports_container.query_items(query, enable_cross_partition_query=True))