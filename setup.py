import setuptools
import io
from os import path

here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
setuptools.setup(
    name="boopy",
    version="0.1",
    author="Xiar Fatah",
    author_email="xiar.fatah@gmail.com",
    description="An educational package for construction of fixed income yield curves.",
    url="https://github.com/Xiar-fatah/boopy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords="term structure, bootstrapping, yield curves, finance",
    install_requires=["dateutil>=2.8.2"],
)
