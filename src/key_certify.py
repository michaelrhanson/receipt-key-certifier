import os
import base64
import M2Crypto
import hashlib
import logging
import time
import cStringIO
import json
import crypto

def NoOp():
	pass

# Generates a keypair and returns a (certificate, privateKey) tuple
def generate_key(bits, expiry_timestamp, price_limit, issuer):

	now = time.time();
	rsaObj = M2Crypto.RSA.gen_key(bits, 0x10001, NoOp)

   	# The certification is a JWT containing a JWK:
   	pubKey = rsaObj.pub() # 2-ple of (exp, mod)
	certificate = {
		"typ": "certified-key",
		"key": 
		[
			{
				"alg": "RSA",
				"mod": base64.b64encode(pubKey[1]),
				"exp": base64.b64encode(pubKey[0])
			}
		],
		"nbf": now,
		"exp": expiry_timestamp,
		"iat": now,
		"price_limit": price_limit,
		"iss": issuer
	}
	serialized = json.dumps(certificate)

	# Certify it:
	certified = crypto.sign_jwt(serialized)

	return (rsaObj.as_pem(None), certified)

