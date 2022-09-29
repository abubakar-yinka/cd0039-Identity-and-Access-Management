import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'udacity-fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'dev'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@DONE implement get_token_auth_header() method
    it should attempt to get the header from the request - DONE
        it should raise an AuthError if no header is present - DONE
    it should attempt to split bearer and the token - DONE
        it should raise an AuthError if the header is malformed - DONE
    return the token part of the header - DONE
'''


def get_token_auth_header():
    auth_token = request.headers.get('Authorization', None)
    # *Check if auth header is present
    if not auth_token:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is required.'
        }, 401)
    
    # *Split auth token header into parts
    auth_token_parts = auth_token.split()
    if auth_token_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'header_malformed',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    elif len(auth_token_parts) == 1:
        raise AuthError({
            'code': 'header_malformed',
            'description': 'JWT Token not added.'
        }, 401)
    elif len(auth_token_parts) > 2:
        raise AuthError({
            'code': 'header_malformed',
            'description': 'Authorization header must contain only "bearer [token]".'
        }, 401)
    
    jwt_token = auth_token_parts[1]
    return jwt_token

'''
@DONE implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload -DONE
        !!NOTE check your RBAC settings in Auth0 - CHECKED
    it should raise an AuthError if the requested permission string is not in the payload permissions array - DONE
    return true otherwise - DONE
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized_action',
            'description': 'Permission not found.'
        }, 403)

    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    raise Exception('Not Implemented')

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator