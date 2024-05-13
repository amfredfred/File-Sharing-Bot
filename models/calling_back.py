from sqlalchemy.orm import sessionmaker 
import hashlib
from database.connection import engine as db_engine
from models import CallbackData, Base


class CallbackDataManager:

    def __init__(self):
        self.db_engine = db_engine
        Base.metadata.create_all(self.db_engine)
        Session = sessionmaker(bind=self.db_engine)
        self.session = Session()

    def generate_callback_data(self, data: str, owner_id):
        data_hash = hashlib.sha256(data.encode()).hexdigest()[:10]
        callback_data = CallbackData(data_hash=data_hash, data=data, owner_id=int(owner_id))
        self.session.add(callback_data)
        self.session.commit()
        return data_hash

    def get_data_from_callback(self, callback):
        callback_data = self.session.query(CallbackData).filter_by(data_hash=callback).first()
        return callback_data.data if callback_data else None

    def remove_callback_data(self, callback):
        callback_data = self.session.query(CallbackData).filter_by(data_hash=callback).first()
        if callback_data:
            self.session.delete(callback_data)
            self.session.commit()
            
hash_exists = CallbackDataManager().get_data_from_callback