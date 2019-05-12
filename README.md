# DigitaslPerfection PC

How to run 

First of all clone this repository.

Then run `start.sh` for deploy postres and iroha Docker containers. Now you in iroha container.

 Then Run

```bash
irohad --config config.docker --genesis_block genesis.block --keypair_name node0 --overwrite_ledger
```

in iroha container. We need this to overwrite ledger. Then the irohad daemon will start and initialize first transaction.

Than install, or check that Iroha and Flask libraries are install for your python 3/


Open new terminal and go to repository directory.


Run `python3 start_server.py` in terminal. It will start the server

Go to http://127.0.0.1:5000 to use DigitalPerfectionPC. Supported names: client, bank, store, warehouse.

Go to http://127.0.0.1:5000/admin to admin page.

[![Proof of work](https://img.youtube.com/vi/pl8wF0pjIU8&/0.jpg)](https://www.youtube.com/watch?v=pl8wF0pjIU8&)
