from setuptools import setup, find_packages

__version__ = "0.1.2"

setup(
    name="slack",
    version=__version__,
    description="Simple Slack CLI client",
    author="Rafał Potempa",
    author_email="rafal.potem@gmail.com",
    url="https://github.com/rafalpotempa/slack-cli",
    scripts=["src/slack"],
    packages=["src"]
)
