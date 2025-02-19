from setuptools import setup, find_packages

from jobfunnel import __version__ as version

description = 'Tool to Analyze current Job Market.'
url = 'https://github.com/ADdream/JobMarket'
requires = ['beautifulsoup4>=4.6.3',
            'HTMLParser >=0.0.2',
            'lxml>=4.2.4',
            'requests>=2.19.1',
            'python-dateutil>=2.8.0',
            'PyYAML>=5.1',
            'scikit-learn>=0.21.2',
            'nltk>=3.4.1',
            'scipy>=1.4.1',
            'pytest>=5.3.1'
            ]

with open('readme.md', 'r') as f:
    readme = f.read()

setup(
    name                          = 'JobMarket',
    version                       = version,
    description                   = description,
    long_description              = readme,
    long_description_content_type = 'text/markdown',
    author                        = 'Varma Kalidhindi',
    author_email                  = 'varma.kalidhindi931@gmail.com',
    url                           = url,
    license                       = 'MIT License',
    python_requires               = '>=3.6.0',
    install_requires              = requires,
    packages                      = find_packages(exclude=('demo',)),
    include_package_data          = True,
    entry_points                  = {'console_scripts': ['funnel = JobMarket.__main__:main']})
