from iroha_lib import Admin, User

admin = Admin("admin", "cpizza")

account = User(f"stock", "cpizza")
admin.add_asset("product", 1000)
admin.transfer_asset(account.nick, "product", 100)

for nick in ["client", "pizzeria", "franchise"]:
    account = User(f"{nick}", "cpizza")
    admin.add_asset("coin", 100)
    admin.transfer_asset(account.nick, "coin", 100)

