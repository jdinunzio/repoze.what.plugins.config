# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
version = '0.2.1'

setup(name='repoze.what.plugins.config',
      version=version,
      description='pastedeploy help methods for repoze.what.',
      long_description=README,
      classifiers=[],
      keywords='wsgi repoze what paste paster pastedeploy',
      author='Jose Dinuncio',
      author_email='jdinunci@uc.edu.ve',
      url='http://github.com/jdinuncio/repoze.what.plugins.config/tree/master',
      license='BSD-derived (see http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(),
      package_data = {'': ['*.txt']},
      include_package_data=True,
      zip_safe=False,
      tests_require=['repoze.what', 'nose'],
      test_suite="nose.collector",
      install_requires=['repoze.what'],
      namespace_packages=['repoze', 'repoze.what', 'repoze.what.plugins'],
      entry_points='''\
      [paste.filter_app_factory]
      config = repoze.what.plugins.config:make_middleware_with_config
      ''',
      )
