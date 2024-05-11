from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import engine as DBEngine
from datetime import datetime

Base = declarative_base()


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey("profiles.id"))
    name = Column(String)
    balance = Column(Float, default=0)
    currency = Column(String)

    transactions = relationship("Transaction", back_populates="wallet")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    amount = Column(Float)
    type = Column(String)
    status = Column(String)
    timestamp = Column(TIMESTAMP)

    wallet = relationship("Wallet", back_populates="transactions")


class WalletManager:
    def __init__(self):
        Base.metadata.create_all(DBEngine)

    def create_wallet(self, telegram_id, name, currency="USD"):
        wallet = Wallet(telegram_id=telegram_id, name=name, currency=currency)
        try:
            DBEngine.session.add(wallet)
            DBEngine.session.commit()
            print("Wallet created successfully.")
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
