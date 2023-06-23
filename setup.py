from setuptools import setup

setup(
  name='torrent-manager',
  version='0.1.0',
  packages=['torrent-manager'],
  install_requires = [
    "Flask >2, <3"
    "requests",
 ],
  license="MIT",
  author="Bryan Alves",
  author_email="bryanalves@gmail.com",
  description="Rule-based torrent deletion using Flood"
)
