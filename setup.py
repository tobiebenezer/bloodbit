from setuptools import setup, find_packages

setup(
    name='bloodbit',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'psycopg2-binary',
        'python-dotenv',
        'flasgger',
        'pydantic',
        'email-validator',
        'Flask-SQLAlchemy',
        'gunicorn',
        'Flask-JWT-Extended',
        'werkzeug'
    ],
)
