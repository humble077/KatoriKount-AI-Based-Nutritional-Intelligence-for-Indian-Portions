from setuptools import setup, find_packages

setup(
    name="katorikount",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.32.0",
        "pandas==2.2.0",
        "google-auth==2.27.0",
        "google-auth-oauthlib==1.2.0",
        "google-auth-httplib2==0.2.0",
        "google-api-python-client==2.118.0"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-Based Nutritional Intelligence for Indian Portions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/katorikount",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 