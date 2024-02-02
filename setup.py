import setuptools

with open("README.md", "r", encoding="utf-8") as handle:
    long_description = handle.read()

with open("requirements.txt", "r", encoding="utf-8") as handle:
    install_requires = [x.strip() for x in handle.readlines()]

setuptools.setup(
    name="math_assist",
    version="0.1.0",
    author="Matthew Jarvis",
    author_email="mattj23@gmail.com",
    description="Tools for helping work out and document math problems, for engineers, scientists, and anyone else",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattj23/math_assist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=install_requires,
)
