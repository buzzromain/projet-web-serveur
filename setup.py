from setuptools import setup

setup(
    name='projet-web-serveur',
    packages=['blog'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)