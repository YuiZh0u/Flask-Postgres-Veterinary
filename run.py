#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys) 
sys.setdefaultencoding('utf8')

from app import app
app.run(debug=True,host="0.0.0.0",port=16001)