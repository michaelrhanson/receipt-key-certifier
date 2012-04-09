import time
import unittest
import json

import receipt_certify
import key_certify

class TestCertifiedReceipts(unittest.TestCase):
	def testGeneration(self):
		now = time.time();

		aReceipt = {
			"typ": "purchase-receipt",
			"product": "http://vendor.com/product/123",
			"user": {
				"type": "directed-identifier",
				"value": "ABCDEFG123456"
			},
			"iss:": "https://coolstore.com/",
			"nbf": now,
			"iat": now,
			"exp": now + 60*60*24*7*14,
			"detail": "https://coolstore.com/receipt_detail/123",
			"verify": "https://coolstore.com/receipt_verify/123"
		}
		serialized = json.dumps(aReceipt)

		certified = receipt_certify.certify_receipt(serialized)
		print certified



class TestCertifiedKey(unittest.TestCase):
	def testGeneration(self):
		now = time.time()
		privateKey, certificate = key_certify.generate_key(1024, now + 60*60*24*14, 5000, "https://coolstore.com/")
		print privateKey
		print certificate

if __name__ == '__main__':
    unittest.main()
