import os.path
import logging
from flask import Flask
import passcheck

log = logging.getLogger('passcheck.passcheckweb')
log.debug('Initializing %s app' % __name__)
app = Flask(__name__.split('.')[0])
checker = passcheck.PassCheck()
log.debug('Initialized PassCheck: %s' % str(checker))


@app.route('/')
def index():
    log.debug('requested index')
    return 'ok'


@app.route('/ping')
def ping():
    log.debug('requested /ping')
    return 'pong'


@app.route('/logs')
def logs():
    log.debug('requested /logs')
    resp = ''
    log_file = os.path.join(os.path.dirname(__file__), 'passcheck.log')
    with open(log_file, 'r') as f:
        for line in f:
            resp += line + '</br >'
    return resp


@app.route('/check/<password>')
def check(password):
    log.debug('requested /check')
    if password in checker:
        log.debug('Found password: %s' % password)
        return 'True'
    else:
        log.debug('Did NOT find password: %s' % password)
        return 'False'
