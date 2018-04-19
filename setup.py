from setuptools import setup

tests_require = [
    'pytest>=3.5.0',
    'pytest-flake8>=1.0.0',
]

setup(
    name='dream',
    version='0.1.0',
    packages=['dream'],
    install_requires=[
        'pyzmq>=16.0.3',
        'scikit-learn>=0.19.1',
        'numpy>=1.13.3',
        'aenum>=2.0.9',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    url='https://github.com/icyblade/dream',
    license='MIT',
    author='Icyblade Dai',
    author_email='icyblade.aspx@gmail.com',
    description='',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
)
