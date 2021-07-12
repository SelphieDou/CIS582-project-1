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

	if platform == 'Ethereum':
		eth_encoded_msg = eth_account.messages.encode_defunct(text=message)
		eth_sig = sig
		eth_pk = pk
		if eth_account.Account.recover_message(eth_encoded_msg,signature = eth_sig) == eth_pk:
			return jsonify(True)
		else:
			return jsonify(False)	
		
	elif platform == 'Algorand':
		result = True 
		return jsonify(True)
		
	else:
		return jsonify(False)

if __name__ == '__main__':
	app.run(port='5002')
