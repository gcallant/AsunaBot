import requests

API_URI = "http://localhost:8000/api"
AUTH_TOKEN = "tiKrW4LfQswOerAVpEMlFhuGQsE8r6YjDd8g6HZFZMlQN5PAvhF2bnqKgX8A"
AUTH_HEADER = {'Authorization' : f'Bearer {AUTH_TOKEN}'}

class ApiException(Exception):
    """Base class for REST API exceptions."""
    pass

class RegistrationConflictException(ApiException):
    """Raised when attempting to register a user who already exists."""
    pass


def getEvents():
    response = requests.get(f'{API_URI}/events', headers=AUTH_HEADER)
    if response.status_code == 200:
        return response.json()['events']
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
        return response.json()
    print("Event update failed: ", response)
    raise ApiException(f'HTTP {response.status_code}\n{response.json()}')

def registerUser(user):
    response = requests.post(f'{API_URI}/register', headers=AUTH_HEADER, data=user)
    if response.status_code == 201:
        return response.json()['data']
    print(f'HTTP Error {response.status_code}')
    raise RegistrationConflictException(f'HTTP {response.status_code}')

if __name__ == '__main__':
    event = getEvent(1)
    event['channel_id'] = "0987654321"
    print(updateEvent(event))

    #raise RegistrationConflictException(getEvent(1))
