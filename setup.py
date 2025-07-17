from setuptools import setup

setup(
    name='xml_flattener',
    version='0.1.1',
    description='ccc1 tool to flatten xml using a xsl template',
    url='https://github.com/ricardogalindo24/xml_flattener',
    author='Ricardo Galindo',
    author_email='jrichardgali@outlook.com',
    license='Apache 2.0',
    packages=['xml_flattener',],
    package_dir={"": "src"},
    package_data={"xml_flattener": ["xslt_example.xslt", "xslt_default.xslt"]},
    include_package_data=True,
    install_requires=['pandas~=2.2.3',
                      'rich~=13.9.4',
                      'lxml~=5.3.0',
                      'typer~=0.16.0',
                      ],
    classifiers=[
                'Development Status :: 3 - Alpha',
                'Intended Audience :: End Users/Desktop',
                'License :: OSI Approved :: BSD License',
                'Operating System :: POSIX :: Linux',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Programming Language :: Python :: 3.5',
            ],
    entry_points = {'console_scripts' : ['xml_flattener = xml_flattener.flattener:run']}
)
