from sqlalchemy.orm import sessionmaker
from database import engine as DBEngine
from helper_func import most_common_word

from models import Searching, Base

class SearchingManager:
    def __init__(self):
        engine = DBEngine
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert_searching(self, chat_id, searched_for):
        searching = Searching(chat_id=chat_id, searched_for=searched_for)
        try:
            self.session.add(searching)
            self.session.commit()
            return True
        except Exception as e:
            print(f"Exception: {e}")
            self.session.rollback()
            return False

    def get_searching_by_searched_for(self, searched_for):
        return (
            self.session.query(Searching)
            .filter(Searching.searched_for == searched_for)
            .first()
        )

    def get_all_searchings(self):
        return self.session.query(Searching).all()

    def delete_searching(self, searched_for):
        try:
            result = (
                self.session.query(Searching)
                .filter(Searching.searched_for == searched_for)
                .delete()
            )
            self.session.commit()
            return result
        except Exception as e:
            print(f"Exception: {e}")
            self.session.rollback()
            return 0

    def most_common_searched_word(self):
        searched_for_texts = [
            search.searched_for for search in self.get_all_searchings()
        ]
        combined_text = " ".join(searched_for_texts)
        return most_common_word(combined_text)
