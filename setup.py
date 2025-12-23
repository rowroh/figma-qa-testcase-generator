#!/usr/bin/env python3
"""
Figma QA TestCase Generator 설치 스크립트
"""

from setuptools import setup, find_packages
import os

# README.md 읽기
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# requirements.txt 읽기
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="figma-qa-testcase-generator",
    version="1.0.0",
    author="QA Engineering Team",
    author_email="qa@example.com",
    description="시니어 QA 엔지니어를 위한 Figma 기반 테스트케이스 자동 생성 도구",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/figma-qa-testcase-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.950",
            "pytest-cov>=4.0.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "figma-qa=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.json", "config/*.yaml", "config/*.txt", "templates/*"],
    },
    zip_safe=False,
    keywords="figma qa testing testcase automation",
    project_urls={
        "Bug Reports": "https://github.com/your-org/figma-qa-testcase-generator/issues",
        "Source": "https://github.com/your-org/figma-qa-testcase-generator",
        "Documentation": "https://figma-qa-testcase-generator.readthedocs.io/",
    },
)

