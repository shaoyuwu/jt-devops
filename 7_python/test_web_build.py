#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__  import print_function

import os,time
import subprocess
import tarfile
import shutil

class release_web:

    def __init__(self,ip_addr):
        self.ip_addr = ip_addr
        self.web_dir = '/usr/local'
        self.backup_dir = '/data/backup/web_bak'

    @property
    def command(self):
        cmd = "{0} {1} {2}".format('/usr/local/bin/npm','run','build:test_180')
        return  cmd

    def npm_build(self,cmd):
        print('Begin npm run build...')
        subprocess.check_call(cmd,shell=True)
        print('rpm build successful')

    def bak_h5_dir(self):
        h5_dir = os.path.join(self.web_dir,'web/www')
        if os.path.exists(h5_dir):
            shutil.move(h5_dir, '/tmp' + '/www')
        

    def update_web(self,home_dir):
        os.chdir(self.web_dir)
        now_time = time.strftime('%Y%m%d-%H%M%S')
        bak_file="web_" + now_time + ".tar.gz"
        with tarfile.open(bak_file,mode='w') as out:
            out.add('web')
        if os.path.exists(self.backup_dir):
            try:
                shutil.move(bak_file,os.path.join(self.backup_dir,bak_file))
            except Exception as err:
                print(err)
            else:
                shutil.rmtree('web')
                shutil.move(os.path.join(home_dir,'dist'),os.path.join(self.web_dir,'web'))
                subprocess.check_call('{0} {1} {2} {3}'.format('chown','-R','nginx:nginx',os.path.join(self.web_dir,'web')),shell=True)
        if os.path.exists('/tmp/www'):
            shutil.move('/tmp/www',os.path.join(self.web_dir,'web/www'))

def main():
    home_dir = os.getcwd()
    obj = release_web('112.33.13.180')
    obj.npm_build(obj.command)
    obj.bak_h5_dir()
    obj.update_web(home_dir)


if __name__ == "__main__":
    main()