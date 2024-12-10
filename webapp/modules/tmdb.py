import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

from typing import Type

TMDB_KEY:str = os.getenv("TMDB_KEY") # URI pra conectar as parada

class TMDB:
    BASE_URL:str = 'https://api.themoviedb.org/3/'
    API_KEY:str = TMDB_KEY
    DEFAULT_LANGUAGE:str="pt-BR"

    @classmethod
    def fetch(cls, param:str):
        url:str = cls.BASE_URL + param
        headers:dict = {
            "accept": "application/json",
            "Authorization": cls.API_KEY
        }
        res:Type[requests.models.Response] = requests.get(url, headers=headers)
        return json.loads(res.text)

    @classmethod
    def authenticate(cls):
        param:str = 'authentication'
        return cls.fetch(param)

    @classmethod
    def search(cls, category:str, query:str, page:int=1):
        """
        Recebe uma categoria (tv ou movie), uma query (nome da obra que está buscando) e a página de busca, que por padrão é 1.
        Retorna a lista de resultados.
        """
        res:dict = cls.fetch("search/{}?query={}&include_adult=false&language={}&page={}".format(
            category,
            query,
            cls.DEFAULT_LANGUAGE,
            page
        ))
        return res["results"]

    @classmethod
    def getByID(cls, category:str, id:str):
        res:dict = cls.fetch("{}/{}?language={}".format(category, id, cls.DEFAULT_LANGUAGE))
        return res
