from setuptools import setup, find_packages

setup(
    name         = 'xysplider',
    version      = '1.1',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = xysplider.settings']},
    scripts = ['bin/test.py']
)