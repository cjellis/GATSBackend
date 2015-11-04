# Import flask and template operators
from flask import Flask

# Import a module / component using its blueprint handler variable (mod_auth)
from app.events.controllers import events as events

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Register blueprint(s)
app.register_blueprint(events)
# app.register_blueprint(xyz_module)
# ..
