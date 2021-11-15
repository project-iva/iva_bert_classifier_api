from flask import Flask, request, jsonify
from token_required_wrapper import token_required
import jwt
import os
from classification_helpers import make_classify


app = Flask(__name__)


@app.route('/classify', methods=['POST'])
@token_required
def make_classification():
  utterance = request.form['utterance']
  classification = app.classify(utterance)
  print(classification)
  return jsonify(classification)


jwt_token = jwt.encode({}, os.environ.get('JWT_SECRET'), algorithm='HS256')
print(f'JWT Token: {jwt_token}')
app.classify = make_classify()
app.run(host='0.0.0.0')