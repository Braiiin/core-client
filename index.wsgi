#!/usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/braiiin.com/client")
sys.path.insert(0,"/var/www/braiiin.com")

from core_client import create_core_app
app = create_core_app(config='ProductionConfig')
app.run(**app.config['INIT'])
