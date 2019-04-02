import requests

API_URI = "http://localhost:8000/api"
AUTH_TOKEN = "z3usV1VCHcnLaUZuOIfvUZ4rt4VuUiQvMYJaLfiC9KIa4dyA1J8gRy5g90EZ"
AUTH_HEADER = {'Authorization' : f'Bearer {AUTH_TOKEN}'}

class ApiException(Exception):
    """Base class for REST API exceptions."""
    pass

class RegistrationConflictException(ApiException):
    """Raised when attempting to register a user who already exists."""
    pass


def getEvents(filters={}):
    response = requests.get(f'{API_URI}/events', headers=AUTH_HEADER, params=filters)
    if response.status_code == 200:
        return response.json()['data']
    print("Multiple event retrieval failed: ", response.json())
    return []

def getEvent(event_id):
    response = requests.get(f'{API_URI}/events/{event_id}', headers=AUTH_HEADER)
    if response.status_code == 200:
        return response.json()['event']
    print("Event retrieval failed: ", response.json())
    return None

def updateEvent(event):
    event_id = event['id']
    response = requests.patch(f'{API_URI}/events/{event_id}', headers=AUTH_HEADER, data=event)
    if response.status_code == 200:
        return response.json()['event']
    print("Event update failed: ", response)
    raise ApiException(f'HTTP {response.status_code}\n{response.json()}')

def registerUser(user):
    response = requests.post(f'{API_URI}/register', headers=AUTH_HEADER, data=user)
    if response.status_code == 201:
        return response.json()['authcode']
    print(f'HTTP Error {response.status_code}')
    raise RegistrationConflictException(f'HTTP {response.status_code}')

def getUsers(filters={}):
    response = requests.get(f'{API_URI}/users', headers=AUTH_HEADER, params=filters)
    if response.status_code == 200:
        return response.json()['data']
    print("Multiple user retrieval failed: ", response.json())
    return []

def getUser(user_id):
    response = requests.get(f'{API_URI}/users/{user_id}', headers=AUTH_HEADER)
    if response.status_code == 200:
        return response.json()['user']
    print("User retrieval failed: ", response.json())
    return None

def updateUser(user):
    user_id = user['id']
    response = requests.patch(f'{API_URI}/users/{user_id}', headers=AUTH_HEADER, data=user)
    if response.status_code == 200:
        return response.json()['user']
    print("User update failed: ", response)
    raise ApiException(f'HTTP {response.status_code}\n{response.json()}')

if __name__ == '__main__':
    # Lazy programmer unit tests
    user = getUser(4)
    user['role'] = "ADMIN"
    print(updateUser(user))
