from .dbElementsInterface import DBElemensInterface
import bcrypt

class User:
    def __init__(self, name, username, email, password, icon=0, banner=0, bio='', followers=[], following=[], watched={}, watchList={}, reviews=[], config={}):
        self.name = name # Nome qualquer
        self.username = username # Nome de usuário (único)
        self.icon = icon # Código do ícone
        self.banner = banner # Código do banner
        self.bio = bio # Bio (até 200 char)
        self.email = email # Email
        self.password =  self.hashpw(password)# Senha...
        self.followers = followers # Quem segue ele (lista de ids)
        self.following = following # Quem ele segue (lista de ids)
        self.watched = watched # Mídias que ele já assistiu, em ordem de preferência
        self.watchList = watchList # Mídias que pretende consumir // está assistindo {estado: pretende assistir | assistindo}
        self.reviews = reviews # Lista com códigos das reviews do usuário
        self.config = config # Configurações de personalização do usuário
        
    def toDict(self):
        """Converte o usuário pra um dicionário (pra poder colocar no db 😉)""" # Abstractmethod vindo de dbElementsInterface
        return {
            "name": self.name,
            "username": self.username,
            "icon": self.icon,
            "banner": self.banner,
            "bio": self.bio,
            "email": self.email,
            "password": self.password,
            "followers": self.followers,
            "following": self.following,
            "watched": self.watched,
            "watchList": self.watchList,
            "reviews": self.reviews,
            "config": self.config
        }

    def hashpw(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    '''Getters e Setters'''

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username


    def get_icon(self):
        return self.icon

    def set_icon(self, icon):
        self.icon = icon


    def get_banner(self):
        return self.banner

    def set_banner(self, banner):
        self.banner = banner


    def get_bio(self):
        return self.bio

    def set_bio(self, bio):
        self.bio = bio


    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email


    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = self.hashpw(password)


    def get_followers(self):
        return self.followers

    def set_followers(self, followers):
        self.followers = followers


    def get_following(self):
        return self.following

    def set_following(self, following):
        self.following = following


    def get_watched(self):
        return self.watched

    def set_watched(self, watched):
        self.watched = watched


    def get_watch_list(self):
        return self.watchList

    def set_watch_list(self, watchList):
        self.watchList = watchList


    def get_reviews(self):
        return self.reviews

    def set_reviews(self, reviews):
        self.reviews = reviews


    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config
