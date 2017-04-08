from flask import Flask
app = Flask(__name__)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/oauth/google')
def oauth():
  pass

if __name__ == "__main__":
  app.run()
