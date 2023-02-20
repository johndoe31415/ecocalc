import setuptools

with open("README.md") as f:
	long_description = f.read()

setuptools.setup(
	name = "ecocalc",
	packages = setuptools.find_packages(),
	version = "${PACKAGE_VERSION}",
	license = "gpl-3.0",
	description = "Game economy calculator for games like Factorio, Satisfactory, or Dyson Sphere Program",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	author = "Johannes Bauer",
	author_email = "joe@johannes-bauer.com",
	url = "https://github.com/johndoe31415/ecocalc",
	download_url = "https://github.com/johndoe31415/ecocalc/archive/${PACKAGE_VERSION}.tar.gz",
	keywords = [ "economy", "calculator" ],
	entry_points = {
		"console_scripts": [
			"ecocalc = ecocalc.__main__:main"
		]
	},
	include_package_data = True,
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.10",
	],
)
