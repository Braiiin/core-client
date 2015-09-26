#!/usr/bin/python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/braiiin.com/client")
sys.path.insert(0,"/var/www/braiiin.com")

from core_client import create_core_app

application = create_core_app(root='core_client', config='ProductionConfig')

if __name__ == "__main__":
    application.run(**application.config['INIT'])
