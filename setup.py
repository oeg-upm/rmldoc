from setuptools import setup, find_packages

setup(
    name='RMLdoc',
    version='0.1',
    packages=find_packages(),
    description='Rmldoc is a tool that generates documentation of RML mappings',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jhon Toledo',
    author_email='ja.toledo@upm.es',
    url='https://github.com/oeg-upm/rmldoc',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: Apache-2.0 license',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        #
    ],
)
