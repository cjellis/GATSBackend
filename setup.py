from distutils.core import setup

setup(
    name='GATSBackend',
    version='1.0',
    description='Backend Server',
    author='Team GATS',
    author_email='ellis.cr@husky.neu.edu',
    url='https://www.python.org/sigs/distutils-sig/',
    packages=['app',
              'app.administrator',
              'app.database',
              'app.dimensions',
              'app.events',
              'app.skills',
              'app.users'
              'DBScripts']
)
