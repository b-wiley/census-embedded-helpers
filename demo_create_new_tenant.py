# INTERNAL USE ONLY

# This script is meant to serve as a demo application to perform the following functions in a matter of seconds:
# 1) Create new workspace (tenant)
# 2) Invite User to workspace with RBAC applied
# 3) Create Source connection - this is using our Product Demo Data in Snowflake
# 4) Creating a Users model

# IF YOU DO PLAN TO USE THIS: Duplicate this script and adjust as needed for the demo.

#------------------------------------------------------------------------------------------------------------------

import requests, json, time

org_token = '<personal access token>'

def new_workspace_setup(org_token):
    
    # Create new workspace within org using org token
    def create_workspace(org_token):
        url = "https://app.getcensus.com/api/v1/workspaces"
        payload = {
            "name": "Demo Client Workspace",
            "notification_emails": [],
            "return_workspace_api_key": True
        }
        headers = {
            "Authorization": "Bearer " + org_token,
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        print(response)
        response_data = response.json()
        print(response_data)
        workspace_api_key = response_data['data']['api_key']
        print(workspace_api_key)
        return workspace_api_key
    
    workspace_api_key = str(create_workspace(org_token))
    time.sleep(1)
    print("Workspace API Key: " + workspace_api_key)


    def create_workspace_user(org_token):
        org_token = org_token
        # Fetch newly created workspace ID
        def get_new_workspace_id(org_token):
            url = "https://app.getcensus.com/api/v1/workspaces"
            headers = {"Authorization": "Bearer " + org_token}
            response = requests.request("GET", url, headers=headers)
            response_data = response.json()
            workspace_id = response_data['data'][0]['id']
            return workspace_id
        workspace_id = str(get_new_workspace_id(org_token))
        print('Workspace ID: ' + workspace_id)

        # Invite new user to workspace
        url = "https://app.getcensus.com/api/v1/workspaces/" + workspace_id + "/invitations"

        payload = {
            "emails": ["<inssert email address here>"],
            "role": "owner"
        }
        headers = {
            "Authorization": "Bearer " + org_token,
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        print(response)
        response_data = response.json()
        print(response_data)
    
    create_workspace_user(org_token)

    # Using the generated workspace API key, add snowflake as a source
    # This snowflake represents the product demo data that can be found here: https://www.notion.so/getcensus/Product-Demo-Data-12f03612946d48db9f2786021df4cc26
    def create_source(workspace_api_key):
        url = "https://app.getcensus.com/api/v1/sources"

        payload = {"connection": {
                "credentials": {
                    "database": "PRODUCT_DEMO_DATA",
                    "account": "iq48949.us-east-1",
                    "warehouse": "CENSUS_WAREHOUSE",
                    "password": "zrd-tre9bkc*MJR4rfz",
                    "port": "5439",
                    "user": "PRODUCT_DEMO_DATA"
                },
                "label": "Snowflake Object for Demo Client",
                "type": "snowflake"
            }}
        headers = {
            "Authorization": "Bearer " + workspace_api_key,
            "Content-Type": "application/json"
        }

        create_source_response = requests.request("POST", url, json=payload, headers=headers)
        create_source_response_data = create_source_response.json()
        source_id = create_source_response_data['data']['id']
        return source_id
   
    source_id = str(create_source(workspace_api_key))
    time.sleep(1)
    print("Source ID" + source_id)

    # Using the newly created Data Source ID, create a new model within the workspace
    # In this case, i'm generating a customers model
    def create_model(workspace_token, source_id):

        url = "https://app.getcensus.com/api/v1/sources/" + source_id +"/models"

        payload = {
            "description": "Customers aggregated from ETL Sources",
            "name": "Demo Client - Customers",
            "query": "SELECT * FROM PRODUCT_DEMO_DATA.SRC_PRODUCT_DEMO_DATA.USER;"
        }
        headers = {
            "Authorization": "Bearer " + workspace_token,
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)
    
    create_model(workspace_api_key, source_id)

new_workspace_setup(org_token)

