import os
import json
import logging
from functools import wraps
from flask import Flask, redirect, render_template, request, send_from_directory, Response, make_response, url_for, current_app

log_file = 'dumpass.log'

def configure_logging(app):
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    configure_logging(app)

    route_paths = [
        '/Abs/', '/aspnet_client/', '/Autodiscover/', '/AutoUpdate/', '/CertEnroll/', '/CertSrv/',
        '/Conf/', '/DeviceUpdateFiles_Ext/', '/DeviceUpdateFiles_Int/', '/ecp/', '/Etc/', '/EWS/',
        '/Exchweb/', '/GroupExpansion/', '/Microsoft-Server-ActiveSync/', '/OAB/', '/ocsp/',
        '/PhoneConferencing/', '/PowerShell/', '/Public/', '/RequestHandler/', '/RequestHandlerExt/',
        '/Rgs/', '/Rpc/', '/RpcWithCert/', '/UnifiedMessaging/'
    ]

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def page_no_access(e):
        return render_template('403.html'), 403

    @app.errorhandler(401)
    def page_auth_required(e):
        return render_template('401.html'), 401

    for path in route_paths:
        app.add_url_rule(path, endpoint=f'{path}_redirect', view_func=lambda: redirect('/'))

    def check_auth(username, password):
        current_app.logger.info(f"{request.base_url}|{username}:{password}")
        return False

    def authenticate():
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        return decorated

    def add_response_headers(headers={}):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                resp = make_response(f(*args, **kwargs))
                h = resp.headers
                for header, value in headers.items():
                    h[header] = value
                return resp
            return decorated_function
        return decorator

    def changeheader(f):
        return add_response_headers({"Server": "Microsoft-IIS/7.5", "X-Powered-By": "ASP.NET"})(f)

    @app.route('/owa/auth/15.1.1466/themes/resources/segoeui-regular.ttf', methods=['GET'])
    @changeheader
    def font_segoeui_regular_ttf():
        return send_from_directory(os.path.join(app.static_folder, 'owa', 'auth', '15.1.1466', 'themes', 'resources'), 'segoeui-regular.ttf', conditional=True)

    @app.route('/owa/auth/15.1.1466/themes/resources/segoeui-semilight.ttf', methods=['GET'])
    @changeheader
    def font_segoeui_semilight_ttf():
        return send_from_directory(os.path.join(app.static_folder, 'owa', 'auth', '15.1.1466', 'themes', 'resources'), 'segoeui-semilight.ttf', conditional=True)

    @app.route('/owa/auth/15.1.1466/themes/resources/favicon.ico', methods=['GET'])
    @changeheader
    def favicon_ico():
        return send_from_directory(os.path.join(app.static_folder, 'owa', 'auth', '15.1.1466', 'themes', 'resources'), 'favicon.ico', conditional=True)

    @app.route('/owa/auth.owa', methods=['GET', 'POST'])
    @changeheader
    def auth():
        ua = request.headers.get('User-Agent')
        ip = request.remote_addr
        if request.method == 'GET':
            return redirect(url_for('owa', _external=True, replaceCurrent=1, reason=3, url=''), 302)
        else:
            passwordText = ""
            password = ""
            username = ""
            if "username" in request.form:
                username = request.form["username"]
            if "password" in request.form:
                password = request.form["password"]
            if "passwordText" in request.form:
                passwordText = request.form["passwordText"]
            current_app.logger.info(f"{request.base_url}|{username}:{password}|{ip}|{ua}")
            return redirect(url_for('owa', _external=True, replaceCurrent=1, reason=2, url=''), 302)

    @app.route('/owa/auth/logon.aspx', methods=['GET'])
    @changeheader
    def owa():
        return render_template("outlook_web.html")

    @app.route('/')
    @app.route('/exchange/')
    @app.route('/webmail/')
    @app.route('/exchange')
    @app.route('/webmail')
    @changeheader
    def index():
        return redirect(url_for('owa', _external=True, replaceCurrent=1, url=''), 302)

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000, host="0.0.0.0")
