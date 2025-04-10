from setuptools import setup, find_packages

setup(
    name='diplom',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'requests',
        'psycopg2-binary',
        'pytest',
    ],
)
