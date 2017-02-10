#!/usr/bin/env python

"""
Render current foreign exchange rates from the European Central Bank as ledger
market values.
"""

from __future__ import (
    division,
    print_function,
)

import argparse
from collections import namedtuple
from contextlib import closing
import datetime
import sys
import xml.etree.cElementTree as ET

try:
    from urllib.request import urlopen
    from io import StringIO
except ImportError:
    from urllib2 import urlopen
    from cStringIO import StringIO


__version__ = '1.0.0'


class EuroFXRef(object):
    """
    Parser for European Central Bank foreign exchange reference (EuroFXRef)
    data.
    """
    NAMESPACE = {
        'eurofxref': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref',
        'gesmes': 'http://www.gesmes.org/xml/2002-08-01'
    }
    URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'

    def __init__(self, rates=None, date=None):
        self._rates = rates or {}
        self.date = date or datetime.date.today()

    @classmethod
    def from_file(cls, file_obj):
        """
        Parse exchange rates from a file object.

        Args:
            file_obj (file): XML data as a file object

        Returns: EuroFXRef
        """
        data = ET.parse(file_obj)
        root = data.getroot()
        rates = {}
        timestamp = root.find('./eurofxref:Cube/eurofxref:Cube[@time]', cls.NAMESPACE).get('time')
        date = datetime.datetime.strptime(timestamp, '%Y-%m-%d').date()
        for entry in root.findall('./eurofxref:Cube/eurofxref:Cube/eurofxref:Cube', cls.NAMESPACE):
            currency = entry.get('currency')
            rate = {
                'base': 'EUR',
                'currency': currency,
                'date': date,
                'rate': float(entry.get('rate')),
            }
            rates[currency] = Rate(**rate)
        return cls(rates, date)

    @classmethod
    def from_string(cls, text):
        """
        Parse exchange rates from an XML string.

        Args:
            text (str): XML data as a string

        Returns: EuroFXRef
        """
        file_obj = StringIO(text)
        return cls.from_file(file_obj)

    @classmethod
    def from_url(cls, url=None):
        """
        Fetch exchange rates from the European Central Bank (ECB) website.

        Args:
            url (str): URL to ECB data (default: EuroFXRef.URL)

        Returns: EuroFXRef
        """
        url = url if url else cls.URL
        with closing(urlopen(url)) as response:
            return cls.from_file(response)

    def exchange(self, variable, fixed='EUR', amount=1):
        """
        Exchange an amount of fixed currency into the given variable currency.

        Args:
            variable (str): symbol of variable currency (currency to buy)
            fixed (str): symbol of fixed currency (currency to sell)
            amount (int or float): amount of fixed currency to sell

        Raises:
            KeyError: either variable or fixed symbol is not known

        Returns: float
        """
        if variable == fixed:
            rate = 1
        elif variable == 'EUR':
            rate = 1/self._rates[fixed].rate
        elif fixed != 'EUR':
            rate = self._rates[variable].rate * 1/self._rates[fixed].rate
        return amount * rate

    def rates(self, fixed='EUR'):
        """
        Return rates based against the given fixed currency.

        Args:
            fixed (str): symbol of fixed currency (currency to sell)

        Returns: list of Rates
        """
        if fixed == 'EUR':
            return self._rates.values()
        rates = []
        for rate in self._rates.values():
            if rate.currency == fixed:
                continue
            rates.append(rate._replace(base=fixed, rate=self.exchange(rate.currency, fixed)))
        euro = Rate(base=fixed, currency='EUR', rate=self.exchange('EUR', fixed), date=self.date)
        rates.append(euro)
        return rates


class Rate(namedtuple('Rate', ['base', 'currency', 'date', 'rate'])):
    """
    A foreign currency exchange rate.

    Fields:
        base (str): symbol of base (i.e., fixed) currency
        currency (str): symbol of variable currency
        date (datetime.date): date of exchange rate
        rate (float): exchange rate
    """
    def __format__(self, fmt):
        if fmt == 'ledger':
            rate = self._replace(rate=1/self.rate)
            return 'P {date} {currency} {base} {rate:.5f}'.format(**rate._asdict())
        return repr(self)


class StoreUppercaseAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.upper())


def parse_args(argv):
    """
    Parse command-line arguments.

    Args:
        argv (list): command-line arguments

    Returns: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'currency',
        action=StoreUppercaseAction,
        nargs='?', default='EUR', help='base currency [%(default)s]'
    )
    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    fx = EuroFXRef.from_url()
    args = parse_args(argv)
    try:
        for rate in sorted(fx.rates(args.currency)):
            print('{:ledger}'.format(rate))
    except KeyError as exc:
        print('error: unknown symbol: {}'.format(exc.message), file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
