#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cygwin: installs cygwin update
# https://github.com/bnomis/cygwin-update
# (c) Simon Blanchard
from __future__ import print_function

import os
import os.path
import subprocess


def launchctl_load(path):
    argv = ['launchctl', 'load', '-w', path]
    try:
        p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print('Exception running %s: %s' % (argv, e))
    else:
        stdout, stderr = p.communicate()
        if stdout:
            print(stdout.decode().strip())
        if stderr:
            print(stderr.decode().strip())
        p.wait()


def install():
    pwd = os.path.abspath(os.path.dirname(__file__))
    fn = 'org.cygwin.update.plist'
    src = os.path.join(pwd, fn)
    destdir = '/Library/LaunchDaemons'
    dest = os.path.join(destdir, fn)
    try:
        os.symlink(src, dest)
    except Exception as e:
        print('Exception making symlink %s -> %s: %s' % (src, dest, e))
    else:
        launchctl_load(dest)


if __name__ == '__main__':
    install()
