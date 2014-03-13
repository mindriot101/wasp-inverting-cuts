#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from MySQLdb.cursors import SSDictCursor
import os
import subprocess as sp
from uncertainties import ufloat

class ObjectStats(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.data.get(key, None)

    def print_summary(self):
        print "Object {}".format(self.obj_id)
        print "\tRadius {}".format(ufloat(self.rplanet_mcmc, self.rplanet_mcmc_err))
        print "\tOrbital period {}".format(self.period)


class HunterPage(object):
    BASE_URL = 'http://wasp.warwick.ac.uk/planets/cands/cand_display.php'

    def __init__(self, data):
        self.obj_id = self.format_param(data.get('obj_id'))
        self.camera_id = self.format_param(data.get('camera_id'))
        self.field = self.format_param(data.get('field'))
        self.tag = self.format_param(data.get('tag'))

        self.browser = os.environ.get('BROWSER', 'firefox')

    def open(self, dry_run=False):
        cmd = [self.browser, self.url]
        if dry_run:
            print ' '.join(cmd)
        else:
            sp.check_call(cmd)
        return self


    @staticmethod
    def format_param(param):
        return str(param).replace(' ', '')

    @property
    def url(self):
        object_params = [
                ('swaspid', self.obj_id),
                ('cam',self.camera_id),
                ('tag', self.tag),
                ('field', self.field)]

        params = '&'.join(['='.join(pair) for pair in object_params])
        return '?'.join([self.BASE_URL, params])



class Query(object):
    def __init__(self):
        self.fname = os.path.join(
                os.path.dirname(__file__),
                'query.sql')
        with open(self.fname) as infile:
            self.contents = infile.read()

    def __str__(self):
        return self.contents

    def perform(self):
        with MySQLdb.connect(db='wasp', user='sw', host='127.0.0.1',
                cursorclass=SSDictCursor) as cursor:

            cursor.execute(str(self))

            for row in cursor:
                yield row

def main():
    query = Query()
    for row in query.perform():
        HunterPage(row).open()
        ObjectStats(row).print_summary()
        raw_input("Press enter for next object")


if __name__ == '__main__':
    main()
