from setuptools import setup, find_packages

version = '0.1dev'

setup(name='oc-tags',
      version=version,
      description="Tagging for opencore content",
      long_description='',
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Plone",
        ],
      keywords='openplans openplans.org topp tagging',
      author='The Open Planning Project',
      author_email='opencore-dev@lists.openplans.org',
      url='http://openplans.org/projects/opencore',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['opencore'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [topp.zcmlloader]
      opencore = opencore.tagging
      """,
      )
