"""
Sample Configuration
--------------------
Everything in this folder is simply a sample configuration. Feel free to
alter it entirely, or even restructure it.
You may wish to keep this file, however.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd()+"/client"))

from client import create_app
from core_client.public.views import public
from core_client.sphere.views import sphere


def create_core_app(**kwargs):
	"""Create a template Flask app"""
	app = create_app(__name__, **kwargs)
	app.register_blueprints(public, sphere)
	return app