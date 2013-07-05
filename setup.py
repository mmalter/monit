from distutils.core import setup
setup(name='monit',
	version='0.1',
	description='A python module for near-term forecasting with bridge equation models',
	author='Michaël Malter',
	author_email='dev@michaelmalter.fr',
	package_dir=['':'src'],
	packages=[''],
	install_requires=[
		'pandas>=0.11'
		]
	)
