import jwt
from cryptography.hazmat.primitives import serialization
from jwt.exceptions import ExpiredSignatureError


# generate keypair:  ssh-keygen -t rsa


payload_data = {
    "sub": "4242",
    "name": "Jessica Temporal",
    "nickname": "Jess"
}
# secret

# CREATE TOKEN

my_secret = 'my_super_secret'

token = jwt.encode(
    payload=payload_data,
    key=my_secret
)

# VERIFY A JWT with PyJWT
# Find out the algorithm used in a JWT, show header
header_data = jwt.get_unverified_header(token)

# decode
jwt.decode(
    token,
    key='my_super_secret',
    algorithms=[header_data['alg'], ]
)


# __________________________________

# keypair

# CREATE TOKEN


private_key = open('.ssh/id_rsa', 'r').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=b'passph')

new_token = jwt.encode(
    payload=payload_data,
    key=key,
    algorithm='RS256'
)

# VERIFY A JWT with PyJWT
# Find out the algorithm used in a JWT, show header
header_data = jwt.get_unverified_header(new_token)

# decode

public_key = open('.ssh/id_rsa.pub', 'r').read()
key = serialization.load_ssh_public_key(public_key.encode())

jwt.decode(jwt=new_token, key=key, algorithms=[header_data['alg'], ])


# ______________________________________________
# Check the Expiration Date on a JWT
# expiration date set in the "past"

token_ex = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsIm5hbWUiOiJKZXNzIFRlbXBvcmFsIiwiZXhwIjoxNTE2MjM5MDIyfQ.uqeQ60enLaCQEZ-7C0d_cgQSrWfgXRQuoB1LZD0j06E'

header_data = jwt.get_unverified_header(token_ex)

# payload = jwt.decode(
#     jwt=token_ex,
#     key='my_super_secret',
#     algorithms=[header_data['alg'], ]
# )

try:
    payload = jwt.decode(
        jwt=token_ex,
        key='my_super_secret',
        algorithms=[header_data['alg'], ]
    )
except ExpiredSignatureError as error:
    print(f'Unable to decode the token, error: {error}')