from abc import ABC, abstractmethod

class DatabaseCRUDInterface(ABC):
    
    @abstractmethod
    def registerUser(user_obj):
        """
        Função: Registrar usuário no banco de dados
        Recebe: Objeto da classe User
        Retorna: None
        """
        pass

    @abstractmethod
    def registerMedia(media_obj):
        """
        Função: Registrar mídia no banco de dados
        Recebe: Objeto da classe Media
        Retorna: None
        """
        pass

    @abstractmethod
    def registerReview(review_obj):
        """
        Função: Registrar review no banco de dados
        Recebe: Objeto da classe Review
        Retorna: None
        """
        pass
    
    @abstractmethod
    def insertionError():
        """
        Função: Retornar erro de inserção no terminal
        Retorna: False
        """
        pass

    @abstractmethod
    def getUserByID(id):
        """
        Função: Recuperar um usuário do banco usando o ID
        Recebe: ID do usuário no banco
        Retorna: Dicionário de usuário (Equivalente à User.toDict())
        """
        pass

    @abstractmethod
    def getUserByUsername(username):
        """
        Função: Recuperar um usuário do banco usando o username
        Recebe: username do usuário no banco
        Retorna: Dicionário de usuário (Equivalente à User.toDict())
        """
        pass

    @abstractmethod
    def getAllUsers():
        """
        Função: Recupera todos os usuários do banco
        Retorna: Lista de dicionários de usuário (Equivalente à uma lista de User.toDict())
        """
        pass

    @abstractmethod
    def getMediaByID(id):
        """
        Função: Recuperar uma mídia do banco usando o ID
        Recebe: ID da mídia no banco (no formato <category>_<api_id>)
        Retorna: Dicionário de mídia (Equivalente à Media.toDict())
        """
        pass

    @abstractmethod
    def getReviewByID(id):
        """
        Função: Recuperar uma review do banco usando o ID
        Recebe: ID da review no banco (no formato <origin_user>_<category>_<api_id>)
        Retorna: Dicionário de review (Equivalente à Review.toDict())
        """
        pass

    @abstractmethod
    def getAllReviews():
        """
        Função: Recupera todas as reviews do banco
        Retorna: Lista de dicionários de review (Equivalente à uma lista de Review.toDict())
        """
        pass
        
    @abstractmethod
    def getReviewsByAuthor(username):
        """
        Função: Recuperar todas as reviews feitas por um determinado usuário
        Recebe: username do usuário alvo
        Retorna: Lista de dicionátios de review (Equivalente à uma lista de Review.toDict())
        """
        pass

    @abstractmethod
    def getReviewsByMedia(media_id):
        """
        Função: Recuperar todas as reviews de uma determinada obra
        Recebe: ID da mídia no banco (no formato <category>_<api_id>)
        Retorna: Lista de dicionários de review (Equivalente à uma lista de Review.toDict())
        """
        pass
        
    @abstractmethod
    def getReviewersByMedia(category, media_id):
        """
        Função: Recuperar todos os usuários que avaliaram uma obra
        Recebe: Categoria da obra no BANCO e ID da obra na API.
        Retorna: Lista de dicionários de usuário (Equivalente à uma lista de User.toDict())
        """
        # ? Quando um usuário marca uma obra como vista, é acrescentada a chave equivalente ao ID da obra (<category>_<api_id>). Essa chave aponta para "False" se a obra foi apenas vista e "True" se a obra foi vista e avaliada.
        pass
        
    @abstractmethod
    def getAllMedia():
        """
        Função: Recuperar todas as mídias do banco.
        Retorna: Lista de dicionários de mídia (Equivalente á uma lista de Media.toDict()).
        """
        pass
     
    @abstractmethod   
    def getWatchedMedia(username):
        """
        Função: Recuperar todas as mídias vistas por um usuário.
        Recebe: username do usuário alvo
        Retorna: Lista de dicionários de mídia (Equivalente á uma lista de Media.toDict()).
        """
        pass
    
    @abstractmethod
    def getFollowersOf(username):
        """
        Função: Recuperar todos os seguidores de um usuário.
        Recebe: username do usuário alvo
        Retorna: Lista de dicionários de usuário (Equivalente á uma lista de User.toDict()).
        """
        pass
    
    @abstractmethod
    def getWhoUserIsFollowing(username):
        """
        Função: Recuperar todos os usuários que um usuário alvo segue.
        Recebe: username do usuário alvo
        Retorna: Lista de dicionários de usuário (Equivalente á uma lista de User.toDict()).
        """
        pass
    
    @abstractmethod
    def getFollowInfo(username):
        """
        Função: Recuperar as informações de followers e following de um usuário alvo.
        Recebe: username do usuário alvo
        Retorna: Dicionário com uma lista de followers e uma de following.
        """
        pass
    
    @abstractmethod
    def getProfileDiary(profile):
        """
        Função: Recuperar o diário de um usuário na ordem cronológica correta.
        Recebe: dicionário de usuário (Equivalente á User.toDict())
        Retorna: Lista de dicionários equivalentes á páginas do diário.
        """
        pass
    
    @abstractmethod
    def editReview(reviewObj):
        """
        Função: Editar uma review no banco.
        Recebe: dicionário de review (Equivalente á Review.toDict())
        Retorna: None.
        """
        pass
    
    @abstractmethod
    def deleteReview(review):
        """
        Função: Deletar review do banco de dados.
        Recebe: dicionário da review (Equivalente á Review.toDict())
        Retorna: None.
        """
        pass
        
    @abstractmethod
    def deleteReviewByID(id):
        """
        Função: Deletar review do banco usando o ID dela.
        Recebe: ID da review no banco (no formato <user_origin>_<category>_<api_id>)
        Retorna: None.
        """
        pass
    
    @abstractmethod
    def refreshUser(user):
        """
        Função: Atualizar usuário no banco.
        Recebe: dicionário de usuário (Equivalente á User.toDict())
        Retorna: None.
        """
        pass
    
    @abstractmethod
    def refreshMedia(media):
        """
        Função: Atualizar mídia no banco.
        Recebe: dicionário de mídia (Equivalente á Media.toDict())
        Retorna: None.
        """
        pass
    
class DatabaseRenderInterface(ABC):
    @abstractmethod
    def getReviewsToRenderHome():
        """
        Função: Gerar uma lista de reviews com as informações necessárias para renderizar a Home page.
        Retorna: Lista de dicionários de review em um formato único que une informações de usuário, mídia e review.
        """
        pass
    
    @abstractmethod
    def getReviewsToRenderProfile(profile):
        """
        Função: Gerar uma lista de reviews com as informações necessárias para renderizar o perfil de um usuário.
        Recebe: Dicionário de usuário (Equivalente à User.toDict())
        Retorna: Lista de dicionários de review em um formato único que une informações do dono do perfil, mídia e review.
        """
        pass
    
    @abstractmethod
    def getReviewsToRenderMedia(category, media_id, username=None):
        """
        Função: Gerar uma lista de reviews com as informações necessárias para renderizar a página de uma mídia.
        Recebe: Categoria no BANCO, ID da API e opcionalmente recebe o username do cliente se estiver logado para saber diferenciar as reviews dele das ademais
        Retorna: Lista de dicionários de review em um formato único que une informações da review, mídia e autor da review.
        """
        pass
    
    @abstractmethod
    def searchMediaByQuery(category, query):
        """
        Função: Realizar uma busca por uma obra em sua respectiva API.
        Recebe: Categoria (que vai revelar a API que deve ser usada) e a query da busca.
        Retorna: Lista de dicionários onde cada dicionário corresponde á uma obra, com suas informações necessárias para renderizar a página de busca.
        """
        pass
    
    @abstractmethod
    def searchSingleMedia(category, id):
        """
        Função: Recuperar informações de uma mídia específica.
        Recebe: categoria da obra e ID dela na API
        Retorna: Dicionário com as informações da obra (Equivalente á MediaModelPage.build(), que faz justamente esse trabalho de estruturar as informações).
        """
        pass