from distutils.core import setup

setup(
    name='EditDistance',
    version='0.1.0',
    author='Benjamin Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['editdistance'],
    license='LICENSE.txt',
    description='Computing edit distance on arbitrary Python sequences.',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
)
