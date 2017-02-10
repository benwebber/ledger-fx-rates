# ledger-fx-rates

Render [current foreign exchange rates](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/index.en.html) from the European Central Bank as [ledger market values](www.ledger-cli.org/3.0/doc/ledger3.html#Commodities-and-Currencies).

**ledger-fx-rates** output is compatible with any software that uses the ledger journal format, including [hledger](http://hledger.org/).

## Install

**ledger-fx-rates** requires Python 2.7 or later and only depends on the standard library.

Download the [latest release](https://github.com/benwebber/ledger-fx-rates/releases/latest) or install with pip:

```
pip install ledger-fx-rates
```

## Usage

Output rates for the Euro (EUR):

```
$ ledger-fx-rates
P 2017-02-09 AUD EUR 0.71608
P 2017-02-09 BGN EUR 0.51130
P 2017-02-09 BRL EUR 0.30004
P 2017-02-09 CAD EUR 0.71347
P 2017-02-09 CHF EUR 0.93703
P 2017-02-09 CNY EUR 0.13622
P 2017-02-09 CZK EUR 0.03701
P 2017-02-09 DKK EUR 0.13450
P 2017-02-09 GBP EUR 1.17523
P 2017-02-09 HKD EUR 0.12055
P 2017-02-09 HRK EUR 0.13388
P 2017-02-09 HUF EUR 0.00324
P 2017-02-09 IDR EUR 0.00007
P 2017-02-09 ILS EUR 0.24952
P 2017-02-09 INR EUR 0.01401
P 2017-02-09 JPY EUR 0.00833
P 2017-02-09 KRW EUR 0.00082
P 2017-02-09 MXN EUR 0.04575
P 2017-02-09 MYR EUR 0.21069
P 2017-02-09 NOK EUR 0.11254
P 2017-02-09 NZD EUR 0.67554
P 2017-02-09 PHP EUR 0.01874
P 2017-02-09 PLN EUR 0.23204
P 2017-02-09 RON EUR 0.22249
P 2017-02-09 RUB EUR 0.01591
P 2017-02-09 SEK EUR 0.10545
P 2017-02-09 SGD EUR 0.66116
P 2017-02-09 THB EUR 0.02671
P 2017-02-09 TRY EUR 0.25325
P 2017-02-09 USD EUR 0.93528
P 2017-02-09 ZAR EUR 0.06974
```

Output rates for a different currency:

```
$ ledger-fx-rates CAD
P 2017-02-09 AUD CAD 1.00365
P 2017-02-09 BGN CAD 0.71664
P 2017-02-09 BRL CAD 0.42053
P 2017-02-09 CHF CAD 1.31334
P 2017-02-09 CNY CAD 0.19092
P 2017-02-09 CZK CAD 0.05187
P 2017-02-09 DKK CAD 0.18852
P 2017-02-09 EUR CAD 1.40160
P 2017-02-09 GBP CAD 1.64720
P 2017-02-09 HKD CAD 0.16897
P 2017-02-09 HRK CAD 0.18764
P 2017-02-09 HUF CAD 0.00454
P 2017-02-09 IDR CAD 0.00010
P 2017-02-09 ILS CAD 0.34973
P 2017-02-09 INR CAD 0.01964
P 2017-02-09 JPY CAD 0.01168
P 2017-02-09 KRW CAD 0.00115
P 2017-02-09 MXN CAD 0.06412
P 2017-02-09 MYR CAD 0.29531
P 2017-02-09 NOK CAD 0.15773
P 2017-02-09 NZD CAD 0.94684
P 2017-02-09 PHP CAD 0.02626
P 2017-02-09 PLN CAD 0.32523
P 2017-02-09 RON CAD 0.31185
P 2017-02-09 RUB CAD 0.02229
P 2017-02-09 SEK CAD 0.14779
P 2017-02-09 SGD CAD 0.92668
P 2017-02-09 THB CAD 0.03744
P 2017-02-09 TRY CAD 0.35496
P 2017-02-09 USD CAD 1.31089
P 2017-02-09 ZAR CAD 0.09775
```

## Tips

### Using `include` to organize your ledger

Append the daily rates to a separate file:

```
$ ledger-fx-rates >> ~/.ledger-fx-rates.dat
```

In your main ledger file, include the file above:

```
include .ledger-fx-rates.dat
```

### Scheduling updates

The ECB updates these rates around 16:00 CET (15:00 UTC) on trading days.

## License

MIT
