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

	#Check if signature is valid
	if platform == 'Ethereum':
		eth_encoded_msg = message
		eth_sig = sig
		eth_pk = pk
		if eth_account.Account.recover_message(eth_encoded_msg,signature=eth_sig) == eth_pk:
			print( "Eth sig verifies!" )
			result = True #Should only be true if signature validates
		else:
			result = False


	elif platform == 'Algorand':
		algo_sig = sig
		algo_pk = pk
		alog_encoded_msg = message
		if algosdk.util.verify_bytes(alog_encoded_msg,algo_sig,algo_pk):
			print( "Algo sig verifies!" )
			result = True #Should only be true if signature validates
		else:
			result = False

	else:
		result = False
	
	return jsonify(result)

#verify()

if __name__ == '__main__':
	app.run(port='5002')
