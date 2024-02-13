# This file contains the WSGI configuration required to serve up your web application
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys
import os
from dotenv import load_dotenv


# add your project directory to the sys.path
project_home = '/home/webscrap/Python-3.11.2/'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path


project_folder = "/home/webscrap/Python-3.11.2/"  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


# import flask app but need to call it "application" for WSGI to work
  # noqa
from app import app as application