from  setuptools import setup, find_packages

setup(name="gfinch",
      packages=find_packages(),
      package_data={"": ["templates/*"]},
      install_requires=['Click',],
      entry_points='''
          [console_scripts]
          ggen=gfinch.ggen:cli
          gmuta=gfinch.gmuta:cli
          gbud=gfinch.gbud:cli
          gprune=gfinch.gprune:cli
          ggraft=gfinch.ggraft:cli
          gnote=gfinch.gnote:cli
      ''',)
