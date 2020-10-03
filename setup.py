from setuptools import find_packages, setup


setup(
    name='textdatasetcleaner',
    version='0.0.2',
    author='Denis Veselov',
    description='Pipeline for cleaning (preprocessing/normalizing) text datasets',
    url='https://github.com/TextDatasetCleaner/TextDatasetCleaner',
    project_urls={
        "Documentation": "https://github.com/TextDatasetCleaner/TextDatasetCleaner",
        "Source Code": "https://github.com/TextDatasetCleaner/TextDatasetCleaner",
        "Bug Tracker": "https://github.com/TextDatasetCleaner/TextDatasetCleaner/issues",
    },
    license='MIT',
    license_files='LICENSE',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Software Development :: Libraries',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
    keywords=[
        'nlp',
        'preprocessing',
        'text analytics',
        'normalization',
        'natural language processing',
        'linguistics',
        'text processing',
        'text mining',
    ],

    entry_points={
        'console_scripts': [
            'tdc = textdatasetcleaner.cli:run',
        ],
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        # FIXME: textacy not provide max version of srsly
        'srsly==1.0.2',
        'tqdm>=4.49.0<5.0.0',
        # FIXME: https://github.com/vzhou842/profanity-check/issues/24
        #        https://github.com/vzhou842/profanity-check/issues/15
        'scikit-learn<=0.20.2',
        'profanity-check==1.0.3',
        'selectolax>=0.2.7,<0.3.0',
        'requests>=2.24.0,<3.0.0',
        'click>=7.1.2,<8.0.0',
        'PyYAML>=5.3.1,<6.0.0',
        'textacy>=0.10.1<1.0.0',
        # FIXME: https://github.com/facebookresearch/fastText/issues/1067
        # ('fasttext @ https://github.com/facebookresearch/fastText/archive/'
        # 'a20c0d27cd0ee88a25ea0433b7f03038cd728459.zip#egg=fasttext-0.9.2'),

        # Run `python setup.py sdist bdist_wheel`:
        # Invalid value for requires_dist. Error: Can't have direct dependency 'fasttext @ ...'
        'fasttext==0.9.2'
    ],
    include_package_data=True,
    python_requires='>=3.6',
)
