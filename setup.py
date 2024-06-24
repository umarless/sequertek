from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sequertek/__init__.py
from sequertek import __version__ as version

setup(
	name="sequertek",
	version=version,
	description="Customisations for Sequertek",
	author="Crisco Consulting",
	author_email="anikets@criscoconsulting.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
