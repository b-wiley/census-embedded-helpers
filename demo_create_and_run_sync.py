# This script is meant to serve as a demo application to perform the following functions in a matter of seconds:
# 1) Grab Source ID in workspace
# 2) Grab Destination ID in workspace
# 3) Create Sync
# 4) Trigger Sync using newly created Sync ID

# IF YOU DO PLAN TO USE THIS: Duplicate this script and adjust as needed for the demo.

#------------------------------------------------------------------------------------------------------------------

import requests, json, time

org_token = '<personal access token>'

workspace_api_key = '<workspace api token>'


def create_sync(workspace_api_key):
    workspace_api_key = workspace_api_key
    def grab_source_id(workspace_api_key):
        url = "https://app.getcensus.com/api/v1/sources"

        headers = {"Authorization": "Bearer " + workspace_api_key}

        response = requests.request("GET", url, headers=headers)
        response_data = response.json()
        source_id = response_data['data'][0]['id']

        print(source_id)
        return source_id
    source_id = str(grab_source_id(workspace_api_key))
    print(source_id)

    def grab_dest_id(workspace_api_key):
        url = "https://app.getcensus.com/api/v1/destinations"

        headers = {"Authorization": "Bearer " + workspace_api_key}

        response = requests.request("GET", url, headers=headers)
        print(response)
        response_data = response.json()
        dest_id = response_data['data'][0]['id']
        
        print(dest_id)
        return dest_id

    dest_id = str(grab_dest_id(workspace_api_key))
    print(dest_id)

    url = "https://app.getcensus.com/api/v1/syncs"

    payload = {
        "cron_expression": "* 1 * * *",
        "destination_attributes": {
            "connection_id": dest_id,
            "object": "contact"
        },
        "label": "Demo Sync",
        "mappings": [
            {
                "from": {
                    "data": "EMAIL",
                    "type": "column"
                },
                "is_primary_identifier": True,
                "to": "email"
            }
        ],
        "operation": "upsert",
        "paused": False,
        "source_attributes": {
            "connection_id": source_id,
            "object": {
                "name": "Demo Client - Customers",
                "type": "model"
            }
        },
        "triggers": {
            "dbt_cloud": {},
            "fivetran": {},
            "sync_sequence": {}
        }
    }
    headers = {
        "Authorization": "Bearer " + workspace_api_key,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    print(response.text)
    response_data = response.json()
    sync_id = response_data['data']['sync_id']
    print(sync_id)
    print(response.text)
    return sync_id

sync_id = str(create_sync(workspace_api_key))

# Use the newly created Sync ID from the create_sync() function to trigger the sync
trigger_sync_id = '<sync id>'

def trigger_sync(sync_id, workspace_api_key):
    url = "https://app.getcensus.com/api/v1/syncs/" + sync_id + "/trigger"

    headers = {"Authorization": "Bearer " + workspace_api_key}

    response = requests.request("POST", url, headers=headers)

    print(response.text)

trigger_sync(trigger_sync_id, workspace_api_key)
