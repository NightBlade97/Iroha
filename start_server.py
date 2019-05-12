from flask import Flask, render_template, request
from iroha_lib import User, Admin

app = Flask(__name__)


def get_account_assets(account):
    user = User(account)
    return user.get_assets()


@app.route("/", methods=["GET", "POST"])
def admin_page():
    if request.method == "POST":
        name = request.form["who"]
        if name == "client":
            return render_template("user.html", **get_account_assets("client"))
        elif name == "store":
            return render_template("store.html", **get_account_assets("store"))
        elif name == "bank":
            return render_template("bank.html", **get_account_assets("bank"))
        elif name == "warehouse":
            return render_template("warehouse.html", **get_account_assets("warehouse"))
        else:
            return "Nick not found"
    else:
        return render_template("name.html")


@app.route("/send/<sender>", methods=["POST"])
def send(sender=None):
    user = User(sender)
    recipient = request.form["recipient"]
    amount = request.form["amount"]
    if sender == "stock" or sender == "admin":
        asset = request.form["asset"]
    else:
        asset = "coin"
    return user.transfer_asset(recipient, asset, amount)


@app.route("/buy", methods=["POST"])
def buy():
    client = User("client")
    store = User("store")
    return f"{client.transfer_asset(store.nick, 'dpcoin', 50)} || {store.transfer_asset(client.nick, 'pc', 1)}"


@app.route("/makepc", methods=["POST"])
def makepc():
    store = User("store")
    return store.exchange_asset("component", 7, "pc", 1)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    admin = Admin("admin")
    if request.method == "POST":
        asset = request.form["asset"]
        amount = request.form["amount"]
        return admin.add_asset(asset, amount)
    else:
        return render_template("admin.html", name="admin", **admin.get_assets())


if __name__ == "__main__":
    app.run(debug=True)
