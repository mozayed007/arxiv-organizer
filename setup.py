from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name='arxiv_organizer',
    version='2.0.0',
    description='AI-powered arXiv paper organizer with smart download, classification, and enrichment features.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='MoZayed',
    license='MIT',
    url='https://github.com/mozayed007/arxiv-organizer',  
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={
        'arxiv_organizer': ['utils/categories.json'],
    },
    entry_points={
        'console_scripts': [
            'arxiv-organizer=arxiv_organizer.__main__:process_papers',
        ],
    },
    install_requires=requirements,
    python_requires='>=3.9',
)