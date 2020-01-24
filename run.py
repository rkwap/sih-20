import os
from app import app,db

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host = "0.0.0.0",debug=True, port=4000)
