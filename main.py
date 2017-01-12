"""`main` is the top level module for your Bottle application."""

# import the Bottle framework
from bottle import Bottle
from bottle import request
import requests

# Create the Bottle WSGI application.
bottle = Bottle()
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

sandbox_url = 'https://api.paypal.com'
token_service = '/v1/identity/tokenservice'
redirect_url = 'https://hackathon-155402.appspot.com'
lipp_url = sandbox_url + '/signin/authorize?response_type=code&scope=https%3A%2F%2Furi.paypal.com%2Fservices%2Fpayments%2Ffuturepayments&redirect_uri=https%3A%2F%2Fhackathon-155402.appspot.com&client_id=AcnzQ3fr47rBqJmxFVpwSBOws7W8Elkk6fJBpF7pfsgG8_FBckr4NQEloEPhVBw3tS0elJ9Azm2jaoSO'


# Define an handler for the root URL of our application.
@bottle.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    code = request.query.code
    auth_headers = {"Authorization",
                    "Basic QWNuelEzZnI0N3JCcUpteEZWcHdTQk93czdXOEVsa2s2ZkpCcEY3cGZzZ0c4X0ZCY2tyNE5RRWxvRVBoVkJ3M3RTMGVsSjlBem0yamFvU086RU9Gc1oxbGRGWUtxbHM3VThaMGh3Q2F1OF80LXRZcDFVck15akZsMHRmTHl0aThlbHIzQWMwZlRSUnp5NnNVMlNLcVZxRk80REVnVUVSRHc="}
    payload = "&".join("grant_type=authorization_code", "code=%s"(code), "redirect_uri=" + redirect_url)
    lipp_resp = requests.post(sandbox_url + token_service, headers=auth_headers, data=payload)
    refresh_token = lipp_resp['refresh_token']
    id_token = lipp_resp['id_token']
    user_data = lipp_resp['id_token']['user-data']
    return 'Hello World:"' + code + '"'


@bottle.post('/<game_id:int>/login')
def lipp(game_id):
    # do a get request : https://www.msmaster.qa.paypal.com/signin/authorize?client_id=AU9Brr7cKnWaL9uFiOlCnwgKaYDO3pa9nvOBhM6qJZCuxCnPMi3VdfPm45qkOrg6L_S5w2hlpmXnSX6V&response_type=code&scope=https://uri.paypal.com/services/payments/futurepayments&redirect_uri=urn:ietf:wg:oauth:2.0:oob&partner_client_id=AcnzQ3fr47rBqJmxFVpwSBOws7W8Elkk6fJBpF7pfsgG8_FBckr4NQEloEPhVBw3tS0elJ9Azm2jaoSO
    # response CODE
    return lipp_url


# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'
