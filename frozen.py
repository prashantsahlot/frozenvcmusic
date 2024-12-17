import os
import time
from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Greeting(Resource):
    def get(self):
        return "Frozen is Up & Running!"

class Ping(Resource):
    def get(self):
        start_time = time.time()
        # You could add any processing logic here if needed
        end_time = time.time()
        response_time = end_time - start_time
        return jsonify(message="pong", response_time=f"{response_time:.6f} seconds")

api.add_resource(Greeting, '/')
api.add_resource(Ping, '/ping')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
