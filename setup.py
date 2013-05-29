from distutils.core import setup

setup(
    name='EditDistance',
    version='0.1.0',
    author='Benjamin Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['editdistance'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Edit distance computation',
    long_description=open('README.txt').read(),
    install_requires=[],
)
