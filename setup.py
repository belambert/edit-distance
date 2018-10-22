from setuptools import setup

setup(
    name='edit_distance',
    version='1.0.3',
    author='Ben Lambert',
    author_email='blambert@gmail.com',
    packages=['edit_distance'],
    license='LICENSE.txt',
    description='Computing edit distance on arbitrary Python sequences.',
    url='https://github.com/belambert/editdistance',
    keywords=['edit', 'distance', 'editdistance', 'levenshtein'],
    test_suite='test.test.TestEditDistance',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License"
    ],
    entry_points={
        'console_scripts': [
            'edit-distance = edit_distance.code:main'
        ]
    }
)
