class MediaModelPage:
    @staticmethod
    def build(title, description, poster_path, score, release_year, banner_path, genre, size):
        return {
            "title": title,
            "description": description,
            "poster_path": poster_path,
            "score": score,
            "release_year": release_year,
            "banner_path": banner_path,
            "genre": genre,
            "size": size
        }