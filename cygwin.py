#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cygwin: updates cygwin mirror using rsync
# https://github.com/bnomis/cygwin-update
# (c) Simon Blanchard
import argparse
import datetime
import os.path
import subprocess
import sys

####
# edit the variables below to suit your needs
#

# curl command
curlcmd = '/usr/bin/curl'

# the rsync command
rsyncmd = '/usr/bin/rsync'

# where to write the files
destdir = '/Volumes/scratch/cygwin'

# where to write logs
logfile = '/var/root/logs/cygwin.log'

# mirror to rsync from
# see mirrors.py for help choosing a mirror
mirror = 'rsync://rsync.gtlib.gatech.edu/cygwin'

# architectures to mirror
# add x86 to the list if you want it
archs = ['x86_64', ]

# user and group to change ownership to after sync
user = 'simonb'
group = 'staff'

#
# end of user variables
####

# version info
version_info = (0, 1, 0)
__version__ = ".".join([str(v) for v in version_info])


def write_log(options, log, exception=None):
    if options.dry_run:
        print(log)
        return
    
    with open(logfile, 'a') as fp:
        fp.write(log + '\n')
        if exception:
            fp.write('%s\n' % exception)


def run_cmd(options, argv):
    if options.dry_run:
        print(' '.join(argv))
        return
    
    try:
        p = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        write_log(options, 'Exception running %s' % argv, exception=e)
    else:
        stdout, stderr = p.communicate()
        if stdout:
            write_log(options, stdout.decode().strip())
        if stderr:
            write_log(options, stderr.decode().strip())
        p.wait()


def download_url(options, url, filename):
    argv = [curlcmd, '-s', '-o', filename, url]
    run_cmd(options, argv)


def download_setup(options, arch):
    url = 'http://cygwin.com/setup' + '-' + arch + '.exe'
    filename = os.path.join(destdir, 'setup-%s.exe' % arch)
    download_url(options, url, filename)


def do_rsync(options, arch):
    argv = [rsyncmd, '-azq', '--delete', '%s/%s' % (mirror, arch), destdir]
    run_cmd(options, argv)


def sync_arch(options, arch):
    download_setup(options, arch)
    do_rsync(options, arch)


def chown(options):
    # set user:group of files
    argv = ['chown', '-R', '%s:%s' % (user, group), destdir]
    run_cmd(options, argv)


def cygwin_update(options):
    write_log(options, '\n------------')
    write_log(options, 'Starting update %s' % datetime.datetime.now())


    for a in archs:
        sync_arch(options, a)

    chown(options)
    
    write_log(options, 'Ending update %s' % datetime.datetime.now())
    write_log(options, '------------\n')


def main(argv):
    program_name = 'macports'
    usage_string = '%(prog)s [options]'
    version_string = '%(prog)s %(version)s' % {'prog': program_name, 'version': __version__}
    description_string = 'macports: updates the installed macports'

    parser = argparse.ArgumentParser(
        prog=program_name,
        usage=usage_string,
        description=description_string,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--version',
        action='version',
        version=version_string
    )
    

    parser.add_argument(
        '--dry-run',
        dest='dry_run',
        action='store_true',
        default=False
    )
    
    options = parser.parse_args(argv)

    cygwin_update(options)
    return 0


def run():
    sys.exit(main(sys.argv[1:]))


if __name__ == '__main__':
    run()

