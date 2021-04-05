from setuptools import setup

setup(
    name='tasks',
    version='1.0',
    py_modules=['tasks'],
    install_requires=[
        'Click'
    ],
    entry_points='''
    [console_scripts]
    tasks=cli:cli
    '''
)

# points to the cli module and cli function
