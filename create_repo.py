#!/usr/bin/env python2
import argparse, json, os, subprocess

with open('config.json') as f:
    config = json.load(f)

parser = argparse.ArgumentParser(description='creates new repository')
parser.add_argument('repo')
parser.add_argument('--local', action="store_true", default=False)
parser.add_argument('--github', action="store_true", default=False)
parser.add_argument('--bitbucket', action="store_true", default=False)
parser.add_argument('--private', action="store_true", default=False)
args = parser.parse_args()

# create bitbucket repo
if args.bitbucket:
    cmd = 'curl -X POST -s -u %s:%s %s -d name=%s%s' % (config['bitbucket']['username'],
                                                        config['bitbucket']['password'],
                                                        'https://api.bitbucket.org/1.0/repositories/',
                                                        args.repo,
                                                        '&is_private=True' if args.private else '')
    output = subprocess.check_output(cmd, shell=True)
    try:
        json.loads(output)
        print 'successfully created %s on bitbucket' % args.repo
    except:
        print 'failed to create %s on bitbucket' % args.repo

# create github repo
if args.github:
    cmd = 'curl -X POST -s -u %s:%s %s -d name=%s%s' % (config['github']['username'],
                                                        config['github']['password'],
                                                        'https://github.com/api/v2/json/repos/create',
                                                        args.repo,
                                                        '&public=0' if args.private else '')
    output = subprocess.check_output(cmd, shell=True)
    try:
        json.loads(output)
        print 'successfully created %s on github' % args.repo
    except:
        print 'failed to create %s on github' % args.repo

# create local repo
if args.local:
    path = os.path.expanduser('~/' + args.repo)
    try:
        os.mkdir(path)
        os.chdir(path)
        subprocess.call('hg init', shell=True)
        if args.github:
            subprocess.call('git init', shell=True)
        print 'successfully created %s locally' % args.repo
    except:
        print 'failed to create %s locally' % args.repo
