Tip Sugar
====

A discord Tip-bot for Sugarchain.

## Demo

![Demo](https://user-images.githubusercontent.com/43717671/57532105-fa58c400-7375-11e9-8730-6d7d4c32399c.gif)

## Usage

Command prefix : `//`

|Command                         |Description                                  |Example                                            |
|--------------------------------|---------------------------------------------|---------------------------------------------------|
|`//info`                        |Show information of Sugarchain.              |                                                   |
|`//help`                        |Show help message.                           |                                                   |
|`//balance`                     |Show your balances.                          |                                                   |
|`//deposit`                     |Show your deposit address.                   |                                                   |
|`//tip (@mention) (amount)`     |Tip specified amount to specified user.      |`//tip @ilmango 3.939`                             |
|`//withdraw (address) (amount)` |Send specified amount to specified address.  |`//withdraw SadvGYb756YaaC355e3RhY6Ef5JNvWNEWc 10` |
|`//withdrawall (address)`       |Send your all balances to specified address. |`//withdrawall SadvGYb756YaaC355e3RhY6Ef5JNvWNEWc` |

### Tips

withdraw-fee is 0.001 SUGAR.

Number of Confirmations is 6 blocks.

Address type is `bech32` (native segwit).

In `withdraw`, amount must be at least 0.5 SUGAR.

You can use Tip Sugar on DM.

You can donate by tip to Tip Sugar. (example : /tip @Tip Sugar 3.939)

The address changes with each deposit, but you can use the previous one. However, it is recommended to use the latest address.

Please do not use Tip Sugar as a receiving address for mining rewards to prevent the increase of load due to the increase of UTXO.

## Licence

[MIT](https://github.com/ilmango-doge/Tip-Sugar/blob/master/LICENSE)

## Digression

As I mentioned above, I develop Tip Sugar as a personal hobby and for studying. So Tip Sugar may contain bad-code.

I would be grateful if you could suggest a better implementation by PR.

## Requirement

* Python 3.5.3 or higher
* [discord.py](https://github.com/Rapptz/discord.py) (rewrite)
* [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc)

```
python3 -m pip install -U discord.py
```

```
python3 -m pip install python-bitcoinrpc
```

## How to run

1. Edit `config.py`

2. Edit configuration file of coind (bitcoin.conf etc.)

```
daemon=1
server=1
rpcuser={same as config.py}
rpcpassword={same as config.py}
addresstype=bech32 #If you want to set bech32 address as default
```

3. Run `tipsugar.py`

```
python3 tipsugar.py
```