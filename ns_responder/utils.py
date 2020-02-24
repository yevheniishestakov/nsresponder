import requests

def get_primary_mgmt_ip(username, password):

    addresses = ("192.168.58.10", "192.168.58.11")

    url = "http://"+addresses[0]+"/nitro/v1/config/hanode/"

    payload = {}
    headers = {
        'X-NITRO-USER': username,
        'X-NITRO-PASS': password,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    if data['hanode'][0]['state'] == 'Primary':
        return addresses[0]
    else:
        return addresses[1]

def isBound(username, password):
    url = "http://"+str(get_primary_mgmt_ip(username,password))+"/nitro/v1/config/lbvserver_responderpolicy_binding/lbvs-responder-test-80?filter=policyname:sorry_page"

    payload = {}
    headers = {
        'X-NITRO-USER': username,
        'X-NITRO-PASS': password
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    return_dict = dict()

    if 'lbvserver_responderpolicy_binding' in data:
        return_dict['bound'] = True
        return_dict['policyname'] = data['lbvserver_responderpolicy_binding'][0]['policyname']
        return_dict['vserver'] = data['lbvserver_responderpolicy_binding'][0]['name']
        return_dict['priority'] = data['lbvserver_responderpolicy_binding'][0]['priority']

        return return_dict
    else:
        return_dict['bound'] = False
        return return_dict

def unbindPolicy(username, password):
    url = "http://"+str(get_primary_mgmt_ip(username,password))+"/nitro/v1/config/lbvserver_responderpolicy_binding/lbvs-responder-test-80?args=policyname:sorry_page"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-NITRO-USER': username,
        'X-NITRO-PASS': password
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)


def getBindingPriority(username, password):
    url = "http://"+str(get_primary_mgmt_ip(username,password))+"/nitro/v1/config/lbvserver_responderpolicy_binding/lbvs-responder-test-80"

    payload = {}
    headers = {
        'X-NITRO-USER': username,
        'X-NITRO-PASS': password
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    # if no policy is bound to VIP return 100 (default binding priority).
    if not 'lbvserver_responderpolicy_binding' in data:
        return 100
    bindings = data['lbvserver_responderpolicy_binding']

    # Iterate over priority values of each binding making a list of them. Then return the lowest value
    # If there is a binding with priority 1 - return None

    prio_list = list()
    index = 0

    for binding in bindings:

        if int(binding['priority']) == 1:
            return None

        prio_list.append(
            int(binding['priority'])
        )
        index += 1

    prio_list.sort()
    print (prio_list)

    return prio_list[0] - 1


def bindPolicy (username, password):
    url = "http://"+str(get_primary_mgmt_ip(username,password))+"/nitro/v1/config/lbvserver_responderpolicy_binding/lbvs-responder-test-80"

    priority = str(getBindingPriority(username,password))

    payload = "{\n\"lbvserver_responderpolicy_binding\":" \
              "{\n\"name\":\"lbvs-responder-test-80\"," \
              "\n\"policyname\":\"sorry_page\"," \
              "\n\"priority\":"+priority+"," \
              "\n\"gotopriorityexpression\":\"END\"," \
              "\n\"bindpoint\":\"REQUEST\"," \
              "\n\"invoke\":false\n}}"

    headers = {
        'Content-Type': 'application/json',
        'X-NITRO-USER': username,
        'X-NITRO-PASS': password
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    data = response.json()

    return data['message']


def saveConfig(username, password):
    url = "http://"+str(get_primary_mgmt_ip(username,password))+"/nitro/v1/config/nsconfig?action=save"

    payload = "{\"nsconfig\":{\n}}"
    headers = {
        'X-NITRO-USER': username,
        'X-NITRO-PASS': password,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
