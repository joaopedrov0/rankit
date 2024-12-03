class MediaModelPage:
    @staticmethod
    def build(category, id, title, description, poster_path, score, release_year, banner_path, genre, size):
        return {
            "category": category,
            "id": id,
            "title": title,
            "description": description,
            "poster_path": poster_path,
            "score": score,
            "release_year": release_year,
            "banner_path": banner_path,
            "genre": genre,
            "size": size
        }