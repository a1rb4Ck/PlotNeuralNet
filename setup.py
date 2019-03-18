from setuptools import setup

setup(name='nnplot',
      version='0.1',
      description='Plot neural networks - easier interface',
      url='https://github.com/jhaux/PlotNeuralNet',
      author='HarisIqbal88, Johannes Haux',
      author_email='johannes.haux@iwr.uni-heidelberg.de',
      license='MIT',
      packages=['nnplot'],
      install_requires=[
          ],
      zip_safe=False,
      scripts=["nnplot/tikzmake.sh"])
