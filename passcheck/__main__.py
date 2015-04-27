import sys
import os.path
import logging
LOG_FILE = os.path.join(os.path.dirname(__file__), 'passcheck.log')
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s %(name)s-%(levelname)s: %(message)s',
    level=logging.DEBUG)
log = logging.getLogger('passcheck.main')
log.addHandler(logging.StreamHandler(sys.stdout))


def main():
    import passcheckweb
    log.info("Running passcheckweb...")
    passcheckweb.app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
