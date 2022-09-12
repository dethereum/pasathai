from setuptools import setup

setup(
    name='thaitoroman',
    entry_points={
        'console_scripts': [
            'thaitoroman = thaitoroman.cli:main',
        ],
    },
    packages=['thaitoroman']
)