

class Chat:

    def __init__(self):
        self.chat_history = []
        pass

    def reset(self):
        self.chat_history = []
        pass

    def add_message(self, sender, text):
        self.chat_history.append({"sender": sender, "text": text})
        pass

    def get_chat_history(self):
        return self.chat_history
        pass

    def get_last_message(self):
        return self.chat_history[-1]
        pass

    def get_last_messages(self, num_messages):
        return self.chat_history[-num_messages:]
        pass
