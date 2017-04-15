from oauth2client.client import flow_from_clientsecrets
import random
import string

def random_state_string(N=32):
  return random_string()

def random_string(N=32):
  return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

def get_flow():
  flow = flow_from_clientsecrets('client_secrets.json',
    scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:5000/oauth/google')
  flow.params['access_type'] = 'offline'
  flow.params['include_granted_scopes'] = "true"
  return flow

