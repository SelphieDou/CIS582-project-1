from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

'''
print("start!")
sample = {'sig': '0x3718eb506f445ecd1d6921532c30af84e89f2faefb17fc8117b75c4570134b4967a0ae85772a8d7e73217a32306016845625927835818d395f0f65d25716356c1c', 
 'payload': 
   {'message': 'Ethereum test message', 
	'pk': '0x9d012d5a7168851Dc995cAC0dd810f201E1Ca8AF', 
	'platform': 'Ethereum'}}
sig = sample['sig']
payload = sample['payload']
message = json.dumps(payload)
platform = payload['platform']
print(sig, platform, message)
print(type(sig))
print(type(platform))
print(type(message))
'''

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
			#result = True #Should only be true if signature validates
			return jsonify(result= True, user_message = message)


	elif platform == 'Algorand':
		algo_sig = sig
		algo_pk = pk
		alog_encoded_msg = message
		if algosdk.util.verify_bytes(alog_encoded_msg,algo_sig,algo_pk):
			print( "Algo sig verifies!" )
			#result = True #Should only be true if signature validates
			return jsonify(result= True, user_message = message)

	else:
		
		return jsonify(result = False, user_message = 'undefined')

#verify()

if __name__ == '__main__':
	app.run(port='5002')
