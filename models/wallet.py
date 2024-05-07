import psycopg2
from datetime import datetime
from database.connection import DBConnection


class Wallet:

    def __init__(self):
        db_connect = DBConnection()
        self.conn = db_connect.conneciton()
        self._create_tables()

    def _create_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS wallets
                                (id SERIAL PRIMARY KEY,
                                    telegram_id INTEGER,
                                    name TEXT,
                                    balance REAL,
                                    currency TEXT,
                                    FOREIGN KEY(telegram_id) REFERENCES profiles(id))"""
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS transactions
                                (id SERIAL PRIMARY KEY,
                                    wallet_id INTEGER,
                                    amount REAL,
                                    type TEXT,
                                    status TEXT,
                                    timestamp TIMESTAMP,
                                    FOREIGN KEY(wallet_id) REFERENCES wallets(id))"""
            )
            self.conn.commit()

    def create_wallet(self, telegram_id, name, currency="USD"):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO wallets (telegram_id, name, balance, currency) VALUES (%s, %s, %s, %s)",
                    (telegram_id, name, 0, currency),
                )
                self.conn.commit()
                print("Wallet created successfully.")
        except psycopg2.Error as e:
            print("Error creating wallet:", e)
            self.conn.rollback()

    def deposit(self, wallet_id, amount):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE wallets SET balance = balance + %s WHERE id = %s",
                    (amount, wallet_id),
                )
                cursor.execute(
                    "INSERT INTO transactions (wallet_id, amount, type, status, timestamp) VALUES (%s, %s, %s, %s, %s)",
                    (wallet_id, amount, "deposit", "confirmed", datetime.now()),
                )
                self.conn.commit()
                print("Deposit successful.")
        except psycopg2.Error as e:
            print("Error depositing funds:", e)
            self.conn.rollback()

    def withdraw(self, wallet_id, amount):
        current_balance = self.get_wallet_balance(wallet_id)
        if current_balance is None:
            print("Wallet does not exist.")
            return

        if current_balance < amount:
            print("Insufficient funds.")
            return

        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE wallets SET balance = balance - %s WHERE id = %s",
                    (amount, wallet_id),
                )
                cursor.execute(
                    "INSERT INTO transactions (wallet_id, amount, type, status, timestamp) VALUES (%s, %s, %s, %s, %s)",
                    (wallet_id, amount, "withdrawal", "confirmed", datetime.now()),
                )
                self.conn.commit()
                print("Withdrawal successful.")
        except psycopg2.Error as e:
            print("Error withdrawing funds:", e)
            self.conn.rollback()

    def transfer(self, sender_id, receiver_id, amount):
        if sender_id == receiver_id:
            print("Sender and receiver wallets cannot be the same.")
            return
        self.withdraw(sender_id, amount)
        self.deposit(receiver_id, amount)

    def get_transactions(self, wallet_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM transactions WHERE wallet_id=%s", (wallet_id,)
                )
                return cursor.fetchall()
        except psycopg2.Error as e:
            print("Error fetching transactions:", e)
            return []

    def get_wallet_balance(self, wallet_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT balance FROM wallets WHERE id=%s", (wallet_id,))
                balance = cursor.fetchone()
                return balance[0] if balance else None
        except psycopg2.Error as e:
            print("Error fetching wallet balance:", e)
            return None

    def close(self):
        self.conn.close()
