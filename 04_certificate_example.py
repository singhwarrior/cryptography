
'''
Reference URL: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

To enable SSL Certificate enablement first created the self-signed certificate using openssl
command as follows: 

openssl req -x509 -newkey rsa:4096 -nodes -out cert.crt -keyout key.pem -days 1
- cert.crt is the self signed certificate 
- key.pem is private key
'''

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    #app.run(ssl_context=('cert.crt', 'key.pem'))
    app.run(ssl_context=('localhost.crt', 'localhost.key'))

