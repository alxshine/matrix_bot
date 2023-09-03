from setuptools import setup

setup(
    name='mbot',
    version='0.1',
    py_modules=['mbot'],
    install_requires=[
        'click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        mbot=mbot:main
    '''
)