# encoding: utf-8

from setuptools import setup, find_packages


if __name__ == "__main__":

    metadata = {
        'name': 'summarize_hours',
        'version': "0.0.1",
        'description': 'Summarize billed hours recorded in a yaml file.',
        'license': 'New BSD',
        'author': 'Robert David Grant',
        'maintainer': 'Robert David Grant',
        'maintainer_email': "rgrant@enthought.com",
        'packages': find_packages(),
        'long_description': open("README.md").read(),
        'platforms': ["Linux", "Mac OS-X"],
        'entry_points': {'console_scripts':
                            ['summarize_hours = '
                             'summarize_hours.summarize_hours:cli'
                             ]},
    }

    setup(**metadata)
