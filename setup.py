from setuptools import find_packages, setup


setup(
    name='textdatasetcleaner',
    entry_points={
        'console_scripts': [
            'tdc=textdatasetcleaner.cli:run',
        ],
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
