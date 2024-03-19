from setuptools import setup, find_packages

setup(
    name='arxiv_organizer',
    version='0.1',
    description='A package to organize arXiv papers',
    author='MoZayed',
    License = 'MIT',
    url='https://github.com/mozayed007/arxiv-organizer',  
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(),
    package_data={
        'arxiv_organizer': ['utils/categories.json'],
    },
    entry_points={
        'console_scripts': [
            'arxiv-organizer=arxiv_organizer.__main__:process_papers',
        ],
    },
    install_requires=[
        'arxiv',
        'requests>=2.25.1',
        'selenium',
        'webdriver_manager',
    ],
)