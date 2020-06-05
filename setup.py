import setuptools

setuptools.setup(
    name="badger",
    version="0.0.1",
    author="jayeshathila",
    author_email="sharma.jayesh52@gmail.com",
    description="Adds badges to readme of all the repos",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "PyInquirer"],
)
