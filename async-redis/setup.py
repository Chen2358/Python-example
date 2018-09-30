# -*- coding:utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = "0.1"

setup(name="async-redis",
      version=VERSION,
      description="Asynchronous Redis client for the Tornado Web Server, only implement AUTH, SELECT, SET, GET command",
      author="shiyanlou",
      author_email="support@shiyanlou.com",
      license="http://www.apache.org/licenses/LICENSE-2.0",
      url="https://www.shiyanlou.com",
      keywords=["Redis", "Tornado"],
      packages=["asyncredis"])
