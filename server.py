#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from bottle import run
import sys, os, time, urllib2, json

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))
import controllers


run(host='127.0.0.1', port=8082, reloader=True, debug=True)
