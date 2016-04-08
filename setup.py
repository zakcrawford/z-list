from setuptools import setup

setup(
    name='zco',
    version='0.1',
    py_modules=['zco'],
    install_requires=[
        'Click',
        'boto3',
        'parallel-ssh'
    ],
    entry_points='''
    [console_scripts]
    zco=zco:cli
    ''',
)
