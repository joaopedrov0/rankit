import requests
import json

class TMDB:
    BASE_URL = 'https://api.themoviedb.org/3/'
    API_KEY = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZTEyYmNkYzc1ODMwOWFlZjU2YWI3YTFmYmQ3YzIyOCIsIm5iZiI6MTczMjUzMzQyMC44MTQ5NzksInN1YiI6IjY3MTNjMjM1ZDViNzkyNmU5NDZmYzQ5NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5qqvtYIG35_50dSBA9dH3FRM9c1Qgep6xTWZ9TcyVyI'
    DEFAULT_LANGUAGE="pt-BR"

    @classmethod
    def fetch(cls, param):
        url = cls.BASE_URL + param
        headers = {
            "accept": "application/json",
            "Authorization": cls.API_KEY
        }
        res = requests.get(url, headers=headers)
        return json.loads(res.text)

    @classmethod
    def authenticate(cls):
        param = 'authentication'
        return cls.fetch(param)

    @classmethod
    def search(cls, category, query, page=1):
        """
        Recebe uma categoria (tv ou movie), uma query (nome da obra que está buscando) e a página de busca, que por padrão é 1.
        Retorna a lista de resultados.
        """
        res = cls.fetch("search/{}?query={}&include_adult=false&language={}&page={}".format(
            category,
            query,
            cls.DEFAULT_LANGUAGE,
            page
        ))
        return res["results"]

    @classmethod
    def getByID(cls, category, id):
        res = cls.fetch("{}/{}?language={}".format(category, id, cls.DEFAULT_LANGUAGE))
        return res
