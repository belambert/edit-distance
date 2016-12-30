from setuptools import setup

setup(
    name='edit_distance',
    version='0.2.3',
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['edit_distance'],
    license='LICENSE.txt',
    description='Computing edit distance on arbitrary Python sequences.',
    url='https://github.com/belambert/editdistance',
    download_url='https://github.com/belambert/editdistance/tarball/0.2.2',
    keywords=['edit', 'distance', 'editdistance', 'levenshtein'],
    test_suite='test.test.TestEditDistance',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License"
    ]
)
