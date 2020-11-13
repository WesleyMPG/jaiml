from setuptools import setup, find_packages

setup(
  name='jaiml',
  version='0.2',
  url='https://github.com/WesleyMPG/jaiml',
  license='MIT',
  author='Wesley S. Santos',
  email='wesley.mprog@gmail.com',
  zip_safe=False,
  packages=find_packages(exclude=['tests']),
  setup_requires=['Jinja2>=2.11.2']
)