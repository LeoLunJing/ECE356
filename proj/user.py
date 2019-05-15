import query
import post
 
class User:
    def __init__(self, 
                 user_id
                 ):
        self.user_id = user_id

    def post(self, content, topics):
        newpost = post.post(self.user_id, content, topics)
        newpost.save()

