from distutils.core import setup

setup(
    name='readmd',
    version='0.0.1',
    description='Make markdown easier to read as plaintext',
    author='Peter Coles',
    author_email='peter@mrcoles.com',
    url='https://github.com/mrcoles/readmd',
    py_modules=['readmd'],
    scripts=['bin/readmd'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
