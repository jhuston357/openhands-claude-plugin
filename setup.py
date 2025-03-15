"""Setup script for openhands-claude-plugin."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="openhands-claude-plugin",
    version="0.1.0",
    author="OpenHands",
    author_email="openhands@all-hands.dev",
    description="OpenHands plugin for direct Claude integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openhands/openhands-claude-plugin",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
        ],
    },
)