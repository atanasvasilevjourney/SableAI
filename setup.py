"""
ScypherAI Setup Script
Comprehensive setup for the Pine Script to Python Backtesting Framework
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sableai",
    version="1.0.0",
    author="SableAI Team",
    author_email="contact@sableai.com",
    description="Pine Script to Python Backtesting Framework with Domain-Driven Design",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/SableAI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "openbb": ["openbb>=4.0.0"],
        "cipher": ["cipher-bt>=0.1.0", "finplot>=1.0.0"],
        "ai": ["openai>=1.0.0"],
        "bta": ["bta-lib>=0.1.0"],
        "all": [
            "openbb>=4.0.0",
            "cipher-bt>=0.1.0",
            "finplot>=1.0.0",
            "openai>=1.0.0",
            "bta-lib>=0.1.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "sableai=strategy_launcher:main",
            "sableai-openbb=openbb_launcher:main",
            "sableai-cipher=cipher_launcher:main",
            "sableai-ai=backtestsh_launcher:main",
            "sableai-bta=bta_launcher:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.yml", "*.yaml"],
    },
    keywords=[
        "trading", "backtesting", "pinescript", "python", "finance", 
        "algorithmic-trading", "quantitative-finance", "domain-driven-design",
        "openbb", "cipher-bt", "bta-lib", "ai", "machine-learning"
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/SableAI/issues",
        "Source": "https://github.com/yourusername/SableAI",
        "Documentation": "https://github.com/yourusername/SableAI#readme",
    },
)
