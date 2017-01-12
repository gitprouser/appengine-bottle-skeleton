"""`main` is the top level module for your Bottle application."""

# import the Bottle framework
from bottle import Bottle
from bottle import route, request, response, template

# Create the Bottle WSGI application.
bottle = Bottle()
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


# Define an handler for the root URL of our application.
@bottle.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    forum_id = request.query.code
    return 'Hello World:"' + forum_id + '"'


@bottle.route('/hello')
def hello_world():
    return "OMG!!!!"

@bottle.post('/<game_id:int>/login')
def lipp(game_id):
    # do a get request : https://www.msmaster.qa.paypal.com/signin/authorize?client_id=AU9Brr7cKnWaL9uFiOlCnwgKaYDO3pa9nvOBhM6qJZCuxCnPMi3VdfPm45qkOrg6L_S5w2hlpmXnSX6V&response_type=code&scope=https://uri.paypal.com/services/payments/futurepayments&redirect_uri=urn:ietf:wg:oauth:2.0:oob&partner_client_id=AcnzQ3fr47rBqJmxFVpwSBOws7W8Elkk6fJBpF7pfsgG8_FBckr4NQEloEPhVBw3tS0elJ9Azm2jaoSO
    # response CODE
    #
    #
    return "hello:" + str(game_id)

# Define an handler for 404 errors.
@bottle.error(404)
def error_404(error):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.'
