# Run a server
from app import app
import os

# Bind to PORT if defined, otherwise default to 5000.
port = int(os.environ.get('PORT', app.config['PORT']))
l_host = app.config['HOST']
app.run(host=l_host, port=port)
