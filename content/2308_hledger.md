Title: hledger failure messages are better than Ledger's
Date: 2023-08-29
Category: Accounting
Summary: About six months ago, I upgraded our family accounts from Ledger to
    `hledger`. The CLI API of `hledger` is better than that of Ledger, the
    feedback received when a balance assertion fails is just one example.

For any new plain text accounting project I always recommend using
[hledger](https://hledger.org/) over
[Ledger](https://ledger-cli.org/index.html).

The main reason is errors and failures are better reported and rendered with
hledger, so let's look at an example - failed balance assertions.

## An erroneous assertion

Given a journal file with a single transaction, which contains an error:

```
2023/08/29 Some person
    Assets:Current         $ 100 = $ 75.73
    Income
```

The error is that the balance of the Current Account is asserted as `$ 75.73`
after the transaction, when it's really `$ 100`.

## Ledger output

Running Ledger, here's the version:

```sh
ledger --version
```

```
Ledger 3.1.3-20190331, the command-line accounting tool

Copyright (c) 2003-2019, John Wiegley.  All rights reserved.

This program is made available under the terms of the BSD Public License.
See LICENSE file included with the distribution for details and disclaimer.
```

Now, let's ask for a balance - this will check the transaction and complain
about the incorrect balance assertion:

```sh
ledger -f ledger.dat bal
```

```
While parsing file "/tmp/ledger.dat", line 2:
While parsing posting:
  Assets:Current         $ 100 = $ 75.73
                                 ^^^^^^^
Error: Balance assertion off by $ -24.27 (expected to see $ 100)
```

I've always found the "off by" amount confusing and find I don't know if the
asserted balance is too low or high.

## hledger's failed assertion

Just confirming my `hledger` version:

```sh
hledger --version
```

```
hledger 1.28, linux-x86_64
```

Now let's run the same balance report with hledger:

```sh
hledger -f ledger.dat bal
```

```
hledger: Error: /tmp/ledger.dat:2:34:
  | 2023-08-29 Some person
2 |     Assets:Current           $ 100 = $ 75.73
  |                                    ^^^^^^^^^
  |     Income                  $ -100

This balance assertion failed.
In account:    Assets:Current
and commodity: $
this balance was asserted:     75.73
but the calculated balance is: 100
a difference of:               -24.27

Consider viewing this account's calculated balances to troubleshoot. Eg:

hledger reg 'Assets:Current$' cur:'\$' -I  # -f FILE
```

For me, this output is:

* Much more clear. It helpfully shows the failing transaction in the error
  message.
* Easier to understand: The asserted balance is compared to the computed
  balance.

## Conclusion

Given that plain text accounting is hard enough to work with at the best of
times, I would always go for a tool that helps me out the most with the
complexity. Right now, that means I'd take hledger over Ledger.
