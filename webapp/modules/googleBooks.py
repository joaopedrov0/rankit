from googleapiclient.discovery import build

class GoogleBooks:
    API_KEY = 'AIzaSyD8eJWCOCFDtMMqO3qVsccu9-8OdHzgbJQ'
    service = build('books', 'v1', developerKey=API_KEY)
        

    @classmethod
    def search_books(cls, query):

        try:
            query = f'intitle:{query} OR intext:{query}'  # Pesquisa no título e descrição
            request = cls.service.volumes().list(q=query, printType='BOOKS', orderBy='relevance', langRestrict='pt') # max_results (adicionar máximo de resultados) | langRestrict='pt' (resultados em pt-br)
            response = request.execute()

            books = []
            if 'items' in response:
                for item in response['items']:
                    volume_info = item.get('volumeInfo', {})

                    translated_info = {
                        'title': volume_info.get('title', 'Título não disponível'),
                        'date': item.get('id', 'ID não disponível'),
                        'id': item.get('id', 'ID não disponível'),
                        'banner': volume_info.get('imageLinks', {}).get('thumbnail', 'Sem banner disponível'),
                        'authors': volume_info.get('authors', ['Autor não disponível']),
                        'publisher': volume_info.get('publisher', 'Editora não disponível'),
                        'release_year': int(volume_info.get('publishedDate', '0').split('-')[0]) if 'publishedDate' in volume_info else 0,
                        'pages': volume_info.get('pageCount', 0),
                        'description': volume_info.get('description', 'Descrição não disponível'),
                        'genres': volume_info.get('categories', ['Gênero não disponível'])
                    }
                    books.append(translated_info)
            return books
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []



# google_books = GoogleBooks()

# search_term = input("Enter search term: ")

# results = google_books.search_books(search_term)

# print("\nSearch results:")
# for i, book in enumerate(results, start=1):
#     print(f"\nBook {i}:")
#     print(f"  Title: {book['title']}")
#     print(f"  ID: {book['id']}")
#     print(f"  Banner: {book['banner']}")
#     print(f"  Authors: {', '.join(book['authors'])}")
#     print(f"  Publisher: {book['publisher']}")
#     print(f"  Release Year: {book['release_year']}")
#     print(f"  Pages: {book['pages']}")
#     print(f"  Description: {book['description']}")
#     print(f"  Genres: {', '.join(book['genres'])}")
