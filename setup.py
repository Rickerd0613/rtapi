from setuptools import setup
setup(
  name = 'rtapi',
  packages = ['rtapi'],
  version = '0.2',
  description = 'Wrapper for RT API',
  author = 'Jacob Rickerd',
  author_email = 'jacobrickerd@gmail.com',
  license='MIT',
  url = 'https://github.com/Rickerd0613/rtapi',
  download_url = 'https://github.com/peterldowns/rtapi/archive/0.2.tar.gz',
  keywords = ['request', 'tracker', 'rt', 'api'],
  install_requires=[
	'requests',
  ],
)
