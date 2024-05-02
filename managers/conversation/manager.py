import json
import os

class ConversationSession:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.current_step = 'start'
        self.next_step = 'end'
        self.prev_step = None

class ConversationManager:
    def __init__(self, filename="conversation_data.json"):
        self.filename = filename
        self.sessions = self.load_sessions()

    def load_sessions(self):
        try:
            with open(self.filename, "r") as file:
                sessions_data = json.load(file)
                sessions = {}
                for chat_id, session_data in sessions_data.items():
                    session = ConversationSession(chat_id)
                    session.__dict__.update(session_data)
                    sessions[chat_id] = session
                return sessions
        except FileNotFoundError:
            return {}

    def save_sessions(self):
        with open(self.filename, "w") as file:
            sessions_data = {
                str(chat_id): session.__dict__
                for chat_id, session in self.sessions.items()
            }
            json.dump(sessions_data, file)

    def get_session(self, chat_id):
        if chat_id not in self.sessions:
            self.sessions[chat_id] = ConversationSession(chat_id)
            self.save_sessions()
        return self.sessions[chat_id]

    def update_session(self, chat_id, current_step, next_step, prev_step):
        session = self.get_session(chat_id)
        session.current_step = current_step
        session.next_step = next_step
        session.prev_step = prev_step
        self.save_sessions()
