import requests
import os
from dotenv import load_dotenv

load_dotenv()


class RawgGames:
    API_KEY = os.getenv('RAWGGAMES_KEY')  # Chave da API pq fodase aparentemente
    BASE_URL = 'https://api.rawg.io/api/games'

    @classmethod
    def search(cls, query):
        try:
            params = {
                'key': cls.API_KEY,
                'page_size': 5,  # Número de resultados que deseja retornar
                'search': query,  # Pesquisa o título do jogo
                'page': 1,  # Página dos resultados
                'languages': 'pt',  # Preferência pela descrição em português
            }
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()  # Levanta erro se a requisição falhar
            data = response.json()
            print(data)
            games = []
            for item in data.get('results', []): # O(n)
                translated_info = {
                    'title': item.get('name', 'Título não disponível'),
                    'id': item.get('id', 'ID não disponível'),
                    'banner': item.get('background_image', 'Sem banner disponível'),
                    'icon': item.get('image', {}).get('icon', 'Sem ícone disponível'),  # Obtém ícone do jogo
                    'description': item.get('description_raw', 'Descrição não disponível'),
                    'release_year': item.get('released', 'Ano de lançamento não disponível').split('-')[0],
                    'genres': [genre['name'] for genre in item.get('genres', [])],
                    'platforms': [platform['platform']['name'] for platform in item.get('platforms', [])],
                    'developer': item.get('developers', [{'name': 'Desenvolvedor não disponível'}])[0]['name'],
                }
                games.append(translated_info)

            return games

        except Exception as e:
            print(f"Erro ao buscar jogos: {e}")
            return []
        
        # Pior Caso: O(n) | Melhor Caso: Ω(1)


# rawg_games = RawgGames()

# search_term = input("Digite o termo de busca: ")

# results = rawg_games.search_games(search_term)
# print(results)

# print("\nResultados da busca:")
# for i, game in enumerate(results, start=1):
#     print(f"\nJogo {i}:")
#     print(f"  Título: {game['title']}")
#     print(f"  ID: {game['id']}")
#     print(f"  Banner: {game['banner']}")
#     print(f"  Ícone: {game['icon']}")
#     print(f"  Descrição: {game['description']}")
#     print(f"  Ano de Lançamento: {game['release_year']}")
#     print(f"  Gêneros: {', '.join(game['genres'])}")
#     print(f"  Plataformas: {', '.join(game['platforms'])}")
#     print(f"  Desenvolvedor: {game['developer']}")
