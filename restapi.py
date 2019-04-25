import requests

class ApiException(Exception):
    """Base class for REST API exceptions."""
    pass

class UnauthenticatedException(ApiException):
    """Raised when the requesting user is not authenticated."""
    pass

class ForbiddenException(ApiException):
    """Raised when the requesting user does not have the sufficient privileges to make the request."""
    pass

class ConflictException(ApiException):
    """Raised when attempting to create a resource that already exists."""
    pass

class RegistrationConflictException(ApiException):
    """Raised when attempting to register a user who already exists."""
    pass

class restservices:

    def __init__(self, api_uri, auth_token):
        self.api_uri = api_uri
        self.auth_token = auth_token
        self.auth_header = {'Authorization' : f'Bearer {self.auth_token}'}

    def getEvents(self, filters={}):
        response = requests.get(f'{self.api_uri}/events', headers=self.auth_header, params=filters)
        if response.status_code == 200:
            return response.json()['data']
        print("Multiple event retrieval failed: ", response.json())
        return []

    def getEvent(self, event_id):
        response = requests.get(f'{self.api_uri}/events/{event_id}', headers=self.auth_header)
        if response.status_code == 200:
            return response.json()['event']
        print("Event retrieval failed: ", response.json())
        return None

    def createEvent(self, event):
        response = requests.post(f'{self.api_uri}/events', headers=self.auth_header, data=event)
        if response.status_code == 201:
            return response.json()['event']
        print('Event creation failed: ', response.json())
        self.handleErrors(response)

    def updateEvent(self, event):
        event_id = event['id']
        response = requests.patch(f'{self.api_uri}/events/{event_id}', headers=self.auth_header, data=event)
        if response.status_code == 200:
            return response.json()['event']
        print("Event update failed: ", response)
        self.handleErrors(response)

    def registerUser(self, user):
        response = requests.post(f'{self.api_uri}/register', headers=self.auth_header, data=user)
        if response.status_code == 201:
            return response.json()['authcode']
        print(f'HTTP Error {response.status_code}')
        raise RegistrationConflictException(f'HTTP {response.status_code}')

    def getUsers(self, filters={}):
        response = requests.get(f'{self.api_uri}/users', headers=self.auth_header, params=filters)
        if response.status_code == 200:
            return response.json()['data']
        print("Multiple user retrieval failed: ", response.json())
        return []

    def getUser(self, user_id):
        response = requests.get(f'{self.api_uri}/users/{user_id}', headers=self.auth_header)
        if response.status_code == 200:
            return response.json()['user']
        print("User retrieval failed: ", response.json())
        return None

    def updateUser(self, user):
        user_id = user['id']
        response = requests.patch(f'{self.api_uri}/users/{user_id}', headers=self.auth_header, data=user)
        if response.status_code == 200:
            return response.json()['user']
        print("User update failed: ", response)
        self.handleErrors(response)

    def getEventSignups(self, event_id):
        response = requests.get(f'{self.api_uri}/events/{event_id}/signups', headers=self.auth_header)
        if response.status_code == 200:
            return response.json()['signups']
        print("Signup retrieval failed: ", response)
        self.handleErrors(response)

    def createSignup(self, signup):
        response = requests.post(f'{self.api_uri}/events/{signup.event_id}/signups', headers=self.auth_header, data=signup)
        if response.status_code == 201:
            return [response.json()['signup'], response.json()['event'], response.json()['info']]
        print("Signup creation failed: ", response)
        self.handleErrors(response)

    def handleErrors(self, response):
        if(response.status_code == 401):
            raise UnauthenticatedException('HTTP 401')
        elif(response.status_code == 403):
            raise ForbiddenException('HTTP 403')
        elif(response.status_code == 409):
            raise ConflictException('HTTP 409')
        else:
            raise ApiException(f'HTTP {response.status_code}\n{response.json()}')


if __name__ == '__main__':
    # Test here
    rest = restservices('http://localhost:8000/api', 'xxxxxxxxxxxxxxxxxxx')
