from setuptools import setup, find_packages

setup(
    name='open_tab_tracker',
    version='0.0.1',
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['main=open_tab_tracker.__main__:main'],
    }
)
