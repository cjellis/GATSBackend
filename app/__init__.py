# Import flask and template operators
from flask import Flask

# Import a module / component using its blueprint handler variable
from app.events.controllers import events as events
from app.administrator.controllers import admin as admin
from app.skills.controllers import skills as skills
from app.dimensions.controllers import dimensions as dimension
from app.users.controllers import users as users
# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Register blueprint(s)
app.register_blueprint(events)
app.register_blueprint(admin)
app.register_blueprint(skills)
app.register_blueprint(dimensions)
app.register_blueprint(users)
