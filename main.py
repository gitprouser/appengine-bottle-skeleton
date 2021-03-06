"""`main` is the top level module for your Bottle application."""

# import the Bottle framework
from bottle import Bottle
from bottle import request
import requests
import logging
import time
import main


# Create the Bottle WSGI application.
bottle = Bottle()
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

sandbox_url = 'https://api.sandbox.paypal.com'
sandbox_web_url = 'https://www.sandbox.paypal.com'


token_service = '/v1/oauth2/token'
user_info_service = '/v1/oauth2/token/userinfo?schema=openid'
payment_endpoint = '/v1/payments/payment'


prepend_str = len('https://www.paypal.com/webapps/auth/identity/user/')

# TODO Place holder to keep the {"user id" : "refresh tokens"}
user_management = {}
user_game_id = {}
cached_game_id = ''

redirect_url = 'https://hackathon-155402.appspot.com'
lipp_url = sandbox_web_url + '/signin/authorize?response_type=code&scope=https%3A%2F%2Furi.paypal.com%2Fservices%2Fpayments%2Ffuturepayments&redirect_uri=https%3A%2F%2Fhackathon-155402.appspot.com&client_id=AfCEGMbuFg_FvwVqX5kOXR6H5mYMurdHwmXgikTBWe2HIbqehI6bni5TuFH3QFDf3I3HhXR_6xk8FF0r'
client_id = 'AfCEGMbuFg_FvwVqX5kOXR6H5mYMurdHwmXgikTBWe2HIbqehI6bni5TuFH3QFDf3I3HhXR_6xk8FF0r'
client_id_secret = 'EMbbA65h6jSzGXb_kMbSsz6zMBFg0lZEk6mICisGGf2ipf6QMd2A82WancAad9GB4_0OXGlYpFFm1DIf'
base64Encoded_clientId_clientSecret = "QWZDRUdNYnVGZ19GdndWcVg1a09YUjZINW1ZTXVyZEh3bVhnaWtUQldlMkhJYnFlaEk2Ym5pNVR1RkgzUUZEZjNJM0hoWFJfNnhrOEZGMHI6RU1iYkE2NWg2alN6R1hiX2tNYlNzejZ6TUJGZzBsWkVrNm1JQ2lzR0dmMmlwZjZRTWQyQTgyV2FuY0FhZDlHQjRfME9YR2xZcEZGbTFESWY="

auth_headers_token_service = {"Authorization": "Basic " + base64Encoded_clientId_clientSecret,
                "Accept-Language": "en_US",
                "Accept": "application/json"}

# Define an handler for the root URL of our application.
@bottle.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    auth_code = request.query.code
    logging.info("auth_code:" + auth_code)


    # Step - 2 of the lipp integration
    logging.info("auth_headers" + str(auth_headers_token_service))
    payload = "&".join(["grant_type=authorization_code",
                        "code=" + auth_code,
                        "redirect_uri=https%3A%2F%2Fhackathon-155402.appspot.com"])
    logging.info("PayLoad:"+ payload)

    logging.info("uri:"+ sandbox_url + token_service)
    logging.info(time.time())
    try:
        r = requests.post(sandbox_url + token_service, headers = auth_headers_token_service, data=payload, verify=False)
    except Exception as e:
        logging.info(e)
    lipp_resp = r.json()
    logging.info(r.headers)
    logging.info(lipp_resp)
    logging.info( "&".join(['access_token:' + lipp_resp['access_token'], "refresh_token:" + lipp_resp['refresh_token']]))

    #  TODO persist refresh token lipp_resp['refresh_token']

    access_token = lipp_resp['access_token']
    refresh_token = lipp_resp['refresh_token']
    auth_headers_user_info = {"Authorization": "Bearer " + access_token,
                              "Accept-Language": "en_US",
                              "Accept": "application/json"}
    # refresh_token, id_token
    # payload = "&".join(["grant_type=refresh_token", "refresh_token=<>"])
    try:
        r = requests.get(sandbox_url + user_info_service, headers = auth_headers_user_info, verify=False)
    except Exception as e:
        logging.info(e)
    user_info_response = r.json()
    logging.info(user_info_response)
    # payer_id - is the uniquie identifier
    payer_id = user_info_response['payer_id']
    user_management[payer_id] = refresh_token
    logging.info("cached_game_id:'" + cached_game_id + "'")
    user_game_id[cached_game_id] = payer_id
    logging.info("user_game_id")
    logging.info(user_game_id)
    # return user_info_response['payer_id']
    return "Authentication complete! Please close this window"


@bottle.get('/<game_id>/get_payer_id')
def get_payer_id(game_id):
    logging.info('user_game_id:')
    logging.info(user_game_id[game_id])
    return user_game_id[game_id]


@bottle.get('/<game_id>/login')
def lipp(game_id):
    # do a get request : https://www.msmaster.qa.paypal.com/signin/authorize?client_id=AU9Brr7cKnWaL9uFiOlCnwgKaYDO3pa9nvOBhM6qJZCuxCnPMi3VdfPm45qkOrg6L_S5w2hlpmXnSX6V&response_type=code&scope=https://uri.paypal.com/services/payments/futurepayments&redirect_uri=urn:ietf:wg:oauth:2.0:oob&partner_client_id=AcnzQ3fr47rBqJmxFVpwSBOws7W8Elkk6fJBpF7pfsgG8_FBckr4NQEloEPhVBw3tS0elJ9Azm2jaoSO
    # response CODE
    main.cached_game_id = game_id
    return lipp_url

@bottle.get('/<payer_id>/access_token')
def refresh_token_exchange(payer_id):
    refresh_token = user_management[payer_id]
    access_token = rt_to_at_exchange(refresh_token)
    logging.info("access_token:'" + access_token + "'")
    return access_token


def rt_to_at_exchange(refresh_token):
    # Step - 2 of the lipp integration
    logging.info("auth_headers" + str(auth_headers_token_service))
    payload = "&".join(["grant_type=refresh_token",
                        "refresh_token=" + refresh_token,
                        "redirect_uri=https%3A%2F%2Fhackathon-155402.appspot.com"])
    logging.info("PayLoad:"+ payload)

    logging.info("uri:"+ sandbox_url + token_service)
    logging.info(time.time())
    try:
        r = requests.post(sandbox_url + token_service, headers = auth_headers_token_service, data=payload, verify=False)
    except Exception as e:
        logging.info(e)
    rt_to_at_resp = r.json()
    logging.info(r.headers)
    logging.info('rt_to_at_exchange_call')
    logging.info(rt_to_at_resp)
    return rt_to_at_resp['access_token']


@bottle.post('/<payer_id>/payment')
def payments(payer_id):
    refresh_token = user_management[payer_id]
    access_token = rt_to_at_exchange(refresh_token)
    logging.info("access_token:'" + access_token + "'")

    payment_headers = {'Content-Type':'application/json', 'Authorization' : 'Bearer ' + access_token}
    logging.info('payment_headers' + str(payment_headers))

    payload = request.POST.get('sale_request')
    logging.info('payload')
    logging.info(payload)
    try:
        r = requests.post(sandbox_url + payment_endpoint, headers=payment_headers, data=payload, verify=False)
    except Exception as e:
        logging.info(e)
    payment_response = r.json()
    logging.info("response headers" + (', '.join("%s=%r" % (key, val) for (key, val) in r.headers.iteritems())))
    logging.info('payment_id' + payment_response['id'])
    return payment_response['id']

# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'
