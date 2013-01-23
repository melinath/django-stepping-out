from setuptools import setup, find_packages

__version__ = __import__('stepping_out').__version__


description = "An app for storing information on dance venues."


setup(
    name="stepping_out",
    version='.'.join([str(v) for v in __version__]),
    url="http://github.com/melinath/django-stepping-out",
    description=description,
    long_description=description,
    maintainer='Stephen Burrows',
    maintainer_email='stephen.r.burrows@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic',
    ],
    platforms=['OS Independent'],
    install_requires=[
        'django>=1.4',
        'Pillow>=1.1.7',
    ]
)
