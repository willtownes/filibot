try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Filibot- a website about Filipino Botany',
    'author': 'Will Townes',
    'url': 'https://github.com/willtownes/filibot',
    'author_email': 'filibot.web@gmail.com',
    'version': '0.1',
    'install_requires': ['nose','web.py'],
    'packages': ['filibot'],
    'scripts': ['bin/app.py'],
    'name': 'filibot'
}

setup(**config)