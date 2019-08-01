from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='ripple-stats-collector',
   version='1.0',
   description='Collects rippled and local operating system stats.',
   license="GPL 3.0",
   long_description=long_description,
   author='Michael Fazio',
   author_email='michaelfazio@me.com',
   url="https://github.com/michaeljfazio/ripple-stats-collector",
   packages=['ripple-stats-collector'],
   install_requires=[]
)