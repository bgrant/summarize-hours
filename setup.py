# encoding: utf-8

from setuptools import setup, find_packages

install_requires = [
    'pyyaml',
]

metadata = {
    'name': 'summarize_hours',
    'version': "0.0.1",
    'description': 'Summarize billed hours recorded in a yaml file.',
    'license': 'New BSD',
    'author': 'Robert David Grant',
    'maintainer': 'Robert David Grant',
    'maintainer_email': "robert.david.grant@gmail.com",
    'packages': find_packages(),
    'install_requires': install_requires,
    'long_description': open("README.md").read(),
    'platforms': ["Linux", "Mac OS-X", "Windows"],
    'entry_points': {'console_scripts':
                        ['summarize_hours = '
                         'summarize_hours.summarize_hours:cli'
                         ]},
}

setup(**metadata)
