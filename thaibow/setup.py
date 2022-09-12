from setuptools import setup

setup(
    name='thaibow',
    entry_points={
        'console_scripts': [
            'thaibow = thaibow.cli:main',
        ],
    },
    include_package_data=True,
    packages=['thaibow']
)