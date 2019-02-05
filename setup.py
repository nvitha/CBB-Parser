from distutils.core import setup

setup(
    name='Kenpom-Parser',
    version='1.0.0.',
    packages=[''],
    url='https://github.com/nvitha/Kenpom-Parser',
    license='Apache 2',
    author='Nick Vitha',
    author_email='nvitha@github.com',
    description='Parse Kenpom.com for current year data and output to a CSV',
    install_requires=['bs4', 'pandas', 'numpy', 'lxml', 'matplotlib', 'requests']
)
