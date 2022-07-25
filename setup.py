import shutil

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

shutil.rmtree("./dist")

setuptools.setup(
    name="BitwiseExpressionSimplifier",
    version="1.0.2",
    author="Wankko Ree",
    author_email="wkr@wkr.moe",
    description="位运算表达式化简器，支持各种你能想到的用法",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/WankkoRee/BitwiseExpressionSimplifier",
    project_urls={
        "Bug Tracker": "https://github.com/WankkoRee/BitwiseExpressionSimplifier/issues",
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    setup_requires=['wheel'],
    python_requires=">=3.7",
)
