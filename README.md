A Certified Application Receipt is a certified proof of purchase, 
from some purchasing authority,
which is cryptographically rooted in a publically-discoverable key.

A receipt is zero or more certificates, followed by a Web Application Receipt.

Both the certificate and Web Application Receipt are encoded as JavaScript Web Tokens.

In BNF, a Certified Application Receipt is:

	certified-app-receipt: 	cert-chain web-app-receipt
	cert-chain:				(certificate '~')*
	certificate:			<JWT>
	web-app-receipt:		<JWT>

where JWT is, as defined in XXX:

	JWT:					header-64 '.' payload-64 '.' signature-64
	header-64:				base-64 encoded JSON text
	payload-64:				base-64 encoded JSON text
	signature-64:			base-64 encoded signed digest value

The payload of a certificate in this chain, following JWT deserialization, must
be a JSON object with fields:

	"typ": "certified-key"
	"key": <JWK>
	"nbf": <timestamp>
	"exp": <timestamp>
	"iat": <timestamp>
	"price_limit": <number>
	"iss": <url>

The nbf, exp, and iat fields follow normal JWT practice.  The "key" field is
a JWK, which means that it will contain an array.  It is expected that it will
contain an object with an "alg" field of "RSA".

In Mozilla's Marketplace, the certificate chain that we create is two levels deep.
The root key (here called "RK") is protected by a hardware security module, and
is used to certify expiring keys (here called "EK").  The root key has no expiration
date, and is only invalidated by administrative action following a serious security
breach.

The expiring keys are used to sign actual Certified Receipts,
and a certificate for those keys is attached to each Certified Receipt.

Code that verifies a Certified Application Receipt must:

1. Verify the signature-and-certificate chain.  This means that each
   JWT in the chain must be properly signed by the key before it in the chain.
   The top-most (first) certificate in the chain must verify against a public
   key retrieved from the Internet by following a key-discovery protocol
   against the domain identified in its "iss" field.

2. Each certificate in the chain must not have expired.

3. The expiry time of each entry in the chain must be less than or equal to the
   expiry time of the certificate above it in the chain.

4. The price of the Web Application Receipt must be less than or equal to the
   price_limit of its immediate certificate parent.


