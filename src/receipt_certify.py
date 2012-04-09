import crypto
import logging
import cStringIO

# Expects a receipt as a serialized string
def certify_receipt(aReceipt):

	# Part one of the certified receipt is
	# our ephemeral key's certificate
	result = cStringIO.StringIO()
	result.write(crypto.get_certificate())
	
	# Delimiter:
	result.write("~")

	# Part two of the certified_receipt is the
	# input receipt, signed with our software key.

	# Sign the receipt with our current ephemeral key
	signed_receipt = crypto.sign_jwt(aReceipt)
	result.write(signed_receipt)

	return result.getvalue()
