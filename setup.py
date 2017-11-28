from setuptools import setup, find_packages

setup(
    name='dream',
    version='0.1.0',
    packages=find_packages(exclude=['test', 'examples']),
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
