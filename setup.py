from setuptools import setup

setup(
    name='edit_distance',
    version='1.0.1',
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['edit_distance'],
    license='LICENSE.txt',
    description='Computing edit distance on arbitrary Python sequences.',
    url='https://github.com/belambert/editdistance',
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
    ],
    entry_points={
        'console_scripts': [
            'edit-distance = edit_distance.code:main'
        ]
    }
)
