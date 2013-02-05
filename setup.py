from distutils.core import setup

setup(
    name='readmd',
    version='0.1.1',
    description='Make markdown easier to read as plaintext',
    author='Peter Coles',
    author_email='peter@mrcoles.com',
    url='https://github.com/mrcoles/readmd',
    py_modules=['readmd'],
    entry_points={
        'console_scripts': [
            'readmd = readmd:command_line_runner',
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        ],
    )
