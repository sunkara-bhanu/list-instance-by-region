import requests
import json

def test_status_200():
    '''
    Description: Check for status code of the api end point with valid input parameters
    and api key
    Assertion: Validate status code as 200
    '''
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    rest_end_point = rest_end_point+"?instance_region=ap-south-1"
    api_key = "HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw1"
    headers = {'Accept': 'application/json',
               'x-api-key': api_key }

    r = requests.get(rest_end_point,headers=headers)
    assert r.status_code == 200

def test_with_query_params(region='ap-south-1'):
    '''
    Description: Check the response with valid instance region and valid api key
    Assertion: Validate response returned from all the instances for the given region
    '''
    valid_response = {
    "total_instances": 0,
    "instance_details": [
        {
            "region": "ap-south-1",
            "count": 0
        }
    ]
    }
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    rest_end_point = rest_end_point+"?instance_region=ap-south-1"
    api_key = "HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw1"
    headers = {'Accept': 'application/json',
               'x-api-key': api_key }

    r = requests.get(rest_end_point,headers=headers)
    response_dict = json.loads(r.text)
    assert valid_response == response_dict

def test_with_query_param_all(region='all'):
    '''
    Description: Check the response with instance region as 'all' and valid api key
    Assertion: Validate response returned from all the instances across regions
    '''
    valid_response = {
    "total_instances": 0,
    "instance_details": [
        {
            "region": "ap-south-1",
            "count": 0
        },
        {
            "region": "eu-north-1",
            "count": 0
        },
        {
            "region": "eu-west-3",
            "count": 0
        },
        {
            "region": "eu-west-2",
            "count": 0
        },
        {
            "region": "eu-west-1",
            "count": 0
        },
        {
            "region": "ap-northeast-3",
            "count": 0
        },
        {
            "region": "ap-northeast-2",
            "count": 0
        },
        {
            "region": "ap-northeast-1",
            "count": 0
        },
        {
            "region": "ca-central-1",
            "count": 0
        },
        {
            "region": "sa-east-1",
            "count": 0
        },
        {
            "region": "ap-southeast-1",
            "count": 0
        },
        {
            "region": "ap-southeast-2",
            "count": 0
        },
        {
            "region": "eu-central-1",
            "count": 0
        },
        {
            "region": "us-east-1",
            "count": 0
        },
        {
            "region": "us-east-2",
            "count": 0
        },
        {
            "region": "us-west-1",
            "count": 0
        },
        {
            "region": "us-west-2",
            "count": 0
        }
    ]
    }
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    rest_end_point = rest_end_point +"?instance_region="+region
    api_key = "HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw1"
    headers = {'Accept': 'application/json',
               'x-api-key': api_key }

    r = requests.get(rest_end_point,headers=headers)
    response_dict = json.loads(r.text)
    assert valid_response == response_dict

def test_with_no_query_params():
    '''
    Description: Check the response with no query parameters and valid api
    Assertion: Validate 400 Bad request is returned from api
    '''
    valid_response = {
	"code" : "400",
	"message" : "Bad Request"
    }
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    api_key = "HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw1"
    headers = {'Accept': 'application/json',
               'x-api-key': api_key }

    r = requests.get(rest_end_point,headers=headers)
    response_dict = json.loads(r.text)
    assert valid_response == response_dict

def test_with_invalid_query_params(region='ap-south-1'):
    '''
    Description: Check the response with invalid query parameter name and 
                valid api key
    Assertion: Validate 400 Bad request is returned from api
    '''
    valid_response = {
    "code" : "400",
    "message" : "Bad Request"
    }
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    rest_end_point = rest_end_point + "?region="+region
    api_key = "HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw1"
    headers = {'Accept': 'application/json',
                'x-api-key': api_key }
    r = requests.get(rest_end_point,headers=headers)
    response_dict = json.loads(r.text)
    print(valid_response == response_dict)

def test_with_invalid_region(region='ap-south-11'):
    '''
    Description: Check the response with valid query parameter name with invalid 
                region and valid api key
    Assertion: Validate 400 Bad request is returned from api
    '''
    valid_response = {
    "code" : "400",
    "message" : "Bad Request"
    }
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    rest_end_point = rest_end_point + "?region="+region
    api_key = "HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw1"
    headers = {'Accept': 'application/json',
                'x-api-key': api_key }
    r = requests.get(rest_end_point,headers=headers)
    response_dict = json.loads(r.text)
    print(valid_response == response_dict)

def test_with_invalid_key(region='ap-south-1'):
    '''
    Description: Check the response with valid query parameter name with valid 
                region and invalid api key
    Assertion: Validate 403 Forbidden is returned from api
    '''
    valid_response = {
    "code" : "403",
    "message" : "Forbidden"
    }
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    rest_end_point = rest_end_point + "?region="+region
    api_key = "HoreP1O2ON1RTKzabsfx61JmrirqyYnE4ROw0Yw"
    headers = {'Accept': 'application/json',
                'x-api-key': api_key }
    r = requests.get(rest_end_point,headers=headers)
    response_dict = json.loads(r.text)
    print(valid_response == response_dict)

def test_with_without_key(region='ap-south-1'):
    '''
    Description: Check the response with valid query parameter name with valid 
                region and no api key
    Assertion: Validate 403 Forbidden is returned from api
    '''
    valid_response = {
    "code" : "403",
    "message" : "Forbidden"
    }
    rest_end_point = "https://b423a19tgi.execute-api.ap-south-1.amazonaws.com/dev/list_ec2"
    rest_end_point = rest_end_point + "?region="+region
    r = requests.get(rest_end_point)
    response_dict = json.loads(r.text)
    print(valid_response == response_dict)
