from setuptools import setup, find_packages

setup(
    name="travel_box_api",  # Remplace par le nom de ton projet
    version="0.0.1",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aigyre Consult",
    author_email="nicolas.antraygues@gmail.com",
    url="https://github.com/antrayguesn/TravelBoxApi",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "numpy",
        "requests",
        "exif",
        "scikit-learn"
    ],
    python_requires=">=3.6",
)
