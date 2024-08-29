from flask import Flask, make_response

app = Flask(__name__)

# Disable debug mode (important for production)
app.config['DEBUG'] = False

@app.after_request
def remove_headers(response):
  headers_to_remove = ['Server', 'X-Powered-By', 'Content-Type']  # Add more headers if needed
  for header in headers_to_remove:
    response.headers.pop(header, None)
  return response

@app.route('/')
def hello_world():
  response = make_response('Hello, World!')
  response.headers['Custom-Header'] = 'My custom header'  # Add custom headers
  return response

# Use environment variables for certificate paths (optional, but recommended)
cert_path = os.environ.get('CERT_PATH', 'cert.pem')
key_path = os.environ.get('KEY_PATH', 'key.pem')

if __name__ == '__main__':
  # Run Gunicorn with SSL context from environment variables
  from gunicorn.app.base import Application

  class CustomApp(Application):
    def init(self, parser, opts, args):
      super().init(parser, opts, args)
      self.cfg.set('ssl_context', (key_path, cert_path))

  app = CustomApp(app)
  app.run()
