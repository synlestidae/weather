from oauth2client.client import flow_from_clientsecrets

def random_state_string(N=32):
  return random_string()

def random_string(N=32):
  return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

def get_flow():
  state = random_state_string()
  flow = flow_from_clientsecrets('client_secrets.json',
    scope='https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/user.emails.read',
    redirect_uri='http://localhost:5000/oauth/google',
    state=state)
  return (flow, state)

