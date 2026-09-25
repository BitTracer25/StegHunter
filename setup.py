"""
Setup configuration for StegHunter CLI tool.

Enables installation as a system command: steg-hunter
"""

from setuptools import setup, find_packages

setup(
    name="steg-hunter",
    version="2.0.0",
    description="Image steganography analysis and LSB tools",
    author="StegHunter Team",
    author_email="info@steghunter.dev",
    url="https://github.com/hackr25/StegHunter",
    license="MIT",
    packages=find_packages(include=["stego", "stego.*"]),
    py_modules=["main"],
    data_files=[(".", ["stego_model.pkl"])],
    include_package_data=True,
    install_requires=[
        "numpy>=1.24.0",
        "Pillow>=9.0.0",
        "scikit-learn>=1.3.0",
        "joblib>=1.2.0",
    ],
    extras_require={
        "web": ["streamlit>=1.30"],
        "desktop": ["PySide6>=6.6", "torch>=2.0"],
        "training": ["pandas>=2.0", "torch>=2.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "steg-hunter=main:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Security",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Video",
    ],
    keywords="steganography forensics detection security image video analysis",
)
