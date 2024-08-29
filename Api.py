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

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))  # Run with SSL context
