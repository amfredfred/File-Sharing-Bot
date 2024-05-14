from database import engine as DBEngine
from datetime import datetime
from models import Transaction, Wallet, Base
from sqlalchemy.orm import sessionmaker


class WalletManager:
    def __init__(self):
        engine = DBEngine
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_wallet(self, owner_id, name, currency="USD"):
        wallet = Wallet(owner_id=owner_id, name=name, currency=currency)
        try:
            DBEngine.session.add(wallet)
            DBEngine.session.commit()
            print("Wallet created successfully.")
            return wallet
        except Exception as e:
            print("Error creating wallet:", e)
            DBEngine.session.rollback()

    def deposit(self, wallet_id, amount):
        wallet = DBEngine.session.query(Wallet).get(wallet_id)
        if not wallet:
            print("Wallet does not exist.")
            return
        try:
            wallet.balance += amount
            transaction = Transaction(
                wallet_id=wallet_id,
                amount=amount,
                type="deposit",
                status="confirmed",
                timestamp=datetime.now(),
            )
            DBEngine.session.add(transaction)
            DBEngine.session.commit()
            print("Deposit successful.")
        except Exception as e:
            print("Error depositing funds:", e)
            DBEngine.session.rollback()

    def withdraw(self, wallet_id, amount):
        wallet = DBEngine.session.query(Wallet).get(wallet_id)
        if not wallet:
            print("Wallet does not exist.")
            return
        if wallet.balance < amount:
            print("Insufficient funds.")
            return
        try:
            wallet.balance -= amount
            transaction = Transaction(
                wallet_id=wallet_id,
                amount=amount,
                type="withdrawal",
                status="confirmed",
                timestamp=datetime.now(),
            )
            DBEngine.session.add(transaction)
            DBEngine.session.commit()
            print("Withdrawal successful.")
        except Exception as e:
            print("Error withdrawing funds:", e)
            DBEngine.session.rollback()

    def transfer(self, sender_id, receiver_id, amount):
        if sender_id == receiver_id:
            print("Sender and receiver wallets cannot be the same.")
            return
        self.withdraw(sender_id, amount)
        self.deposit(receiver_id, amount)

    def get_transactions(self, wallet_id):
        try:
            transactions = (
                DBEngine.session.query(Transaction)
                .filter(Transaction.wallet_id == wallet_id)
                .all()
            )
            return transactions
        except Exception as e:
            print("Error fetching transactions:", e)
            return []

    def get_wallet_balance(self, wallet_id):
        try:
            wallet = DBEngine.session.query(Wallet).get(wallet_id)
            return wallet.balance if wallet else None
        except Exception as e:
            print("Error fetching wallet balance:", e)
            return None
