from sqlalchemy.orm import sessionmaker
from database import engine as DBEngine
from models import Post, Base


class PostManager:
    def __init__(self):
        engine = DBEngine
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert_post(
        self,
    ):
        post = Post()
        self.session.add(post)
        self.session.commit()
        return True

    def get_post_by_telegram_id(self, telegram_id):
        return (
            self.session.query(Post)
            .filter(Post.owner_id == int(telegram_id))
            .all()
        )

    def get_all_posts(self):
        return self.session.query(Post).all()

    def delete_post(self, telegram_id):
        post = None
        if post:
            self.session.delete(post)
            self.session.commit()
            return 1
        return 0

    

    def update_post(
        self,
    ):
        post = None
        if post:

            self.session.commit()
            return True
        else:
            return False
