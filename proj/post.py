import query

class post:
    def __init__(self, user_id, content, topics):
        self.postBy = user_id
        self.content = content
        self.topics = topics

    def save(self):
        query.insert_post(self)

