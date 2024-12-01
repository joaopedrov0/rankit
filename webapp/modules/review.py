class Review:
    def __init__(self, data, author_id):
        self.data = data
        self.next = None
        self.author_id = author_id