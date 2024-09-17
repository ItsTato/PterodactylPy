from setuptools import setup, find_packages

setup(
    name="pterodactyl",
    version="0.0.4",
    description="A Python wrapper for the Pterodactyl API.",
    author="ItsTato",
    author_email="thatpogcomputer@gmail.com",
    url="https://github.com/ItsTato/PterodactylPy",
    packages=find_packages(),
    install_requires=[
		"requests>=2.32.3"
	],
    classifiers=[
        "Programming Language :: Python :: 3",
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)