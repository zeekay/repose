#!/usr/bin/env python
import zmq

def hook(ui, repo, **kwargs):
    context = zmq.Context()
    client = context.socket(zmq.PUSH)
    client.connect('tcp://127.0.0.1:12987')
    client.send(repo.origroot)

def server():
    import logging, os, subprocess

    logging.basicConfig(filename='pusher.log',level=logging.INFO)

    context = zmq.Context()
    server = context.socket(zmq.PULL)
    server.bind('tcp://127.0.0.1:12987')

    while True:
        repo = server.recv()
        path = os.path.expanduser('~/' + repo)
        os.chdir(path)
        logging.info(subprocess.check_output('hg up', shell=True))
        try:
            logging.info(subprocess.check_output('hg push ssh://bb/zeekay/' + repo, shell=True))
            logging.info('push to bitbucket successful')
        except Exception as e:
            logging.error('push to bitbucket failed: %s' % str(e))
        if os.path.isdir(path + '/.hg/git'):
            try:
                logging.info(subprocess.check_output('hg bookmark -f -r default master', shell=True))
                logging.info(subprocess.check_output('hg push git+ssh://gh/zeekay/' + repo + '.git', shell=True))
                logging.info('push to github successful')
            except Exception as e:
                logging.error('push to gitbub failed: %s' % str(e))

if __name__ == '__main__':
    server()
