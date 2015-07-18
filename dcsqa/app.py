#
# refer to http://flask.pocoo.org/docs/0.10/quickstart/
#

from flask import Flask
from flask.ext.cache import Cache

from criteria import criteria_blueprint
from raw import raw_blueprint
from result import result_blueprint
from auth import auth

app = Flask(__name__)


def _get_url_prefix(request_type, version='v1'):
    """return example would be /zenoss/v1/criteria
    """
    return '/{kind}/{version}/{request_type}'.\
        format(kind=app.config['KIND'], version=version, request_type=request_type)


def create_app(app_name='dcsqa', config='config.DevelopmentConfig'):
    app.config.from_object(config)
    app.cache = Cache(app) 

    # register blueprint for each restful entry
    # http://flask.pocoo.org/docs/0.10/blueprints/
    app.register_blueprint(criteria_blueprint, url_prefix=_get_url_prefix('criteria'))
    app.register_blueprint(raw_blueprint, url_prefix=_get_url_prefix('raw'))
    app.register_blueprint(result_blueprint, url_prefix=_get_url_prefix('result'))

    return app


@app.route('/')
def index():
    return 'please use API'


@app.route('/login')
@auth.login_required
def login():
    return 'welcome!'