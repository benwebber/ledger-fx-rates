# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name='ledger-fx-rates',
    version='1.0.0',
    url='https://github.com/benwebber/ledger-fx-rates/',

    description='Render current foreign exchange rates from the European Central Bank as ledger market values.',
    long_description=open('README.md').read(),

    author='Ben Webber',
    author_email='benjamin.webber@gmail.com',

    py_modules=['ledger_fx_rates'],

    zip_safe=False,

    entry_points={
        'console_scripts': [
            'ledger-fx-rates = ledger_fx_rates:main',
        ],
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
