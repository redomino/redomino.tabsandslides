from setuptools import setup, find_packages
import os

version = '0.7'

setup(name='redomino.tabsandslides',
      version=version,
      description="jquerytools tabs and slide implementations",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        ],
      keywords='Zope Plone Views',
      author='Maurizio Lupo',
      author_email='maurizio.lupo@redomino.com',
      url='http://pypi.python.org/pypi/redomino.tabsandslides',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redomino'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'lxml'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
