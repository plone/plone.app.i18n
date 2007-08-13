from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='plone.app.i18n',
      version=version,
      description="Plone specific i18n extensions.",
      long_description="""\
""",
      classifiers=[
        'Framework :: Plone',
        'Framework :: Zope2',
      ],
      keywords='Plone i18n',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.app.i18n',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
      )
