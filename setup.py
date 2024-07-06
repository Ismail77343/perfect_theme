from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in perfect_theme/__init__.py
from perfect_theme import __version__ as version

setup(
	name="perfect_theme",
	version=version,
	description="perfect_theme",
	author="ismail",
	author_email="himiismail123@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
