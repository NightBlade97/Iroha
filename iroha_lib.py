import binascii
from iroha import Iroha, IrohaCrypto, IrohaGrpc
from os import path

net = IrohaGrpc()


def send_transaction_and_return_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print(
        "Transaction hash = {}, creator = {}".format(
            hex_hash, transaction.payload.reduced_payload.creator_account_id
        )
    )
    net.send_tx(transaction)
    return list(net.tx_status_stream(transaction))


class IrohaClient:
    def __init__(self, nick: str, domain: str = "digperf"):
        self.nick = nick
        self.domain = domain
        with open(
            path.join("ledger_config", f"{self.nick}@{self.domain}.priv"), "r"
        ) as privk:
            self._private_key = str.encode(privk.read())

        with open(
            path.join("ledger_config", f"{self.nick}@{self.domain}.pub"), "r"
        ) as pubk:
            self.public_key = str.encode((pubk.read()))
        self.iroha = Iroha(f"{self.nick}@{self.domain}")

    def __str__(self):
        return f"{self.nick}, {self.domain}, {self._private_key}, {self.public_key}"


class User(IrohaClient):
    def transfer_asset(self, recipient, asset, amount):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "TransferAsset",
                    src_account_id=f"{self.nick}@{self.domain}",
                    dest_account_id=f"{recipient}@{self.domain}",
                    asset_id=f"{asset}#{self.domain}",
                    description="transfer",
                    amount=str(amount),
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, self._private_key)
        return str(send_transaction_and_return_status(tx))

    def get_assets(self):
        query = self.iroha.query(
            "GetAccountAssets", account_id=f"{self.nick}@{self.domain}"
        )
        IrohaCrypto.sign_query(query, self._private_key)

        response = net.send_query(query)
        data = response.account_assets_response.account_assets
        result = {}
        for asset in data:
            result[asset.asset_id.split("#")[0]] = str(asset.balance)
        for a in ["component", "pc", "dpcoin"]:
            result.setdefault(a, 0)
        return result

    def exchange_asset(
        self, asset_from: str, amount_from: int, asset_to: str, amount_to: str
    ):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "SubtractAssetQuantity",
                    asset_id=f"{asset_from}#{self.domain}",
                    amount=str(amount_from),
                ),
                self.iroha.command(
                    "AddAssetQuantity",
                    asset_id=f"{asset_to}#{self.domain}",
                    amount=str(amount_to),
                ),
            ]
        )
        IrohaCrypto.sign_transaction(tx, self._private_key)
        return str(send_transaction_and_return_status(tx))


class Admin(User):
    def add_asset(self, asset: str, amount: int):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "AddAssetQuantity",
                    asset_id=f"{asset}#{self.domain}",
                    amount=str(amount),
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, self._private_key)
        return str(send_transaction_and_return_status(tx))

    def del_asset(self, asset: str, amount: int):
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "SubtractAssetQuantity",
                    asset_id=f"{asset}#{self.domain}",
                    amount=str(amount),
                )
            ]
        )
        IrohaCrypto.sign_transaction(tx, self._private_key)
        return str(send_transaction_and_return_status(tx))

    def create_account(self, nick: str) -> User:
        user = User(nick, self.domain)
        tx = self.iroha.transaction(
            [
                self.iroha.command(
                    "CreateAccount",
                    account_name=user.nick,
                    domain_id=user.domain,
                    public_key=user.public_key,
                )
            ]
        )

        IrohaCrypto.sign_transaction(tx, self._private_key)
        send_transaction_and_return_status(tx)
        return user

