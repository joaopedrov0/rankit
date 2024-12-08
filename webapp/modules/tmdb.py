import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()
TMDB_KEY = os.getenv("TMDB_KEY") # URI pra conectar as parada

class TMDB:
    BASE_URL = 'https://api.themoviedb.org/3/'
    API_KEY = TMDB_KEY
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
