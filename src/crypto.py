#
# Wrapper for crypto functions
#

import M2Crypto
import hashlib
import logging
import jwt

class KeyStore(object):
	def sign(self, data, hash):
		self.key.reset_context(hash)
		self.key.sign_init()
		self.key.sign_update(data)
		return self.key.sign_final()

	def encode_jwt(self, payload):
		return jwt.encode(payload, self, u'RS256')

	def load_cert(self, name):
		try:
			crtFP = open("%s.crt" % name, "r")
			crt = crtFP.read()
			crtFP.close()
			self.certificate = crt
		except Exception, e:
			logging.error("Unable to load certificate for key '%s': cannot find '%s.crt' file in working directory" % (name, name))
			raise IOError("Unable to load certificate for key '%s'" % name)		


# Fallback keystore for testing:
class SoftwareKeyStore(KeyStore):
	def __init__(self):
		pass
	
	def setKey(self, name):
		self.key = M2Crypto.EVP.load_key("%s.pem" % name)
		self.load_cert(name)

# The real keystore:
class CHILKeyStore(KeyStore):
	def __init__(self):
		M2Crypto.Engine.load_dynamic()
		self.engine = M2Crypto.Engine.Engine("chil")
		self.engine.set_default(M2Crypto.m2.ENGINE_METHOD_RSA)
		logging.debug("Loaded hardware engine \"%s\"" % self.engine.get_name())
	
	def setKey(self, name):
		self.key = self.engine.load_private_key(name)
		self.load_cert(name)

KEYSTORE = SoftwareKeyStore()		#CHILKeyStore()
KEYSTORE.setKey("test_key")			#"test1"

def __init__():
	pass

def sign(input_data):
	return KEYSTORE.sign(input_data, "sha256")

def sign_jwt(input_data):
	return KEYSTORE.encode_jwt(input_data)

def get_certificate():
	return KEYSTORE.certificate
