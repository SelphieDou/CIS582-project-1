from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
	content = request.get_json(silent=True)
	sig = content['sig']
	payload = content['payload']
	platform = payload['platform']
	message = json.dumps(payload)
	pk = payload['pk']
	result = False

	#Check if signature is valid
	if platform == 'Ethereum':
		result = True #Should only be true if signature validates

	elif platform == 'Algorand':
		result = False #Should only be true if signature validates

	return jsonify(result)

if __name__ == '__main__':
	app.run(port='5002')
