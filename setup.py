from distutils.core import setup

setup(
    name='EditDistance',
    version='0.1.0',
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['editdistance'],
    license='LICENSE.txt',
    description='Computing edit distance on arbitrary Python sequences.',
    long_description=open('README.md').read(),
    url='https://github.com/belambert/editdistance',
    download_url = 'https://github.com/belambert/editdistance/tarball/0.1', 
    keywords=['edit', 'distance', 'levenshtein'],
    classifiers = [],
)
