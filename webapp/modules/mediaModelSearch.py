class MediaModelSearch:
    @staticmethod
    def build(category, id, title, description, poster_path, score, release_year):
        return {
            "category": category,
            "id": id,
            "title": title,
            "description": description,
            "poster_path": poster_path,
            "score": score,
            "release_year": release_year
        }