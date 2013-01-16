from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

import pymongo
from urlparse import urlparse

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    ###
    session_factory = UnencryptedCookieSessionFactoryConfig('..session_key..')
    authn_policy = AuthTktAuthenticationPolicy('seekrit', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    db_url = urlparse(settings['mongo_uri'])
    conn = pymongo.Connection(host = db_url.hostname,port = db_url.port)
    ###
    config = Configurator(settings=settings,session_factory=session_factory，
        authentication_policy=authn_policy,authorization_policy=authz_policy)
    ####
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.registry.settings['db_conn'] = conn

    def add_mongon_db(event):
        settings = event.request.registry.settings
        db = settings['db_conn'][db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        event.request.db = db

    config.add_subscriber(add_mongon_db,NewRequest)
    config.add_route('user_register', 'users/register')
    config.add_route('user_login', 'users/login')
    config.scan()
    return config.make_wsgi_app()
