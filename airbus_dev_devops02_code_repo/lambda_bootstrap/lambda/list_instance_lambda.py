import json
import boto3

import boto3
from botocore.config import Config

def list_regions(service):
    """ Function to list the AWS available regions

    Args:
        service (string): Service associated required AWS regions

    Returns:
        list : List of AWS available regions for given input service
    """
    regions = []    
    client = boto3.client(service)
    response = client.describe_regions()
    regions = [item["RegionName"] for item in response['Regions']]
    return regions


def lambda_handler(event,context):
    """ Function to list the EC2 instances deployed across available regions

    Args:
        event (list): List of events received from the caller
        context (list): List of methods associated with the caller

    Returns:
        json : Json response comprising the total instances across regions along
               with individual region wise instances
    """
    
    instance_region = event['instance_region']
    allowed_instance_states = ["pending", "running", "shutting-down", "terminated", "stopping" , "stopped" ]
    allowed_regions = list_regions("ec2")
    
    # Define the default response
    final_response = {
                    'total_instances' : 0,
                    'instance_details' : 
                    [{
                        'region' : 'NA',
                        'count' : 0
                    }
                    ]
                }
                
    # Default error response
    retVal = {
                    "body": 'Invalid Input',
                    "type": "Error"
             }
              
    # if instance region is not provided look for instances across all the available aws regions available
    if (instance_region == "all"):
        instance_region = list_regions("ec2")
    else:
        if instance_region not in allowed_regions:
            raise Exception(json.dumps(retVal))
        elif len(instance_region) == 0:
            raise Exception(json.dumps(retVal))
        instance_region = []
        instance_region.append(event['instance_region'])

    
    # Adjust the list size within default response to accomodate required out parameters
    final_response['instance_details'] = final_response['instance_details'] * len(instance_region)

    # Check status of EC2 in each region
    global_cnt = 0
    iter_cnt = 0
    
    for region in instance_region:
        reg_cnt = 0
        
        # Change regions with config
        cur_config = Config(region_name=region)
        client = boto3.client("ec2", config=cur_config)
        response = client.describe_instances()

        for r in response["Reservations"]:
            status = r["Instances"][0]["State"]["Name"]
            for i in range(len(allowed_instance_states)):
                if allowed_instance_states[i] == status:
                    # Increment total instances acorss regions
                    global_cnt += 1
                    
                    # Increment instances within region
                    reg_cnt +=1
        
        # Add result to the final response
        final_response['instance_details'][iter_cnt] = {'region': region, 'count' : reg_cnt}
        iter_cnt +=1

        
    final_response['total_instances'] = global_cnt
    # final_response = json.dumps(final_response)
    return final_response
