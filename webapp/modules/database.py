from utils import db, UsersCollection, MediaCollection, ReviewsCollection
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

'''Special parameters to collections funcs
$push: Insert at an array
$set: Add new key:value to an object
$and: Check for two conditions (AND operator)
$or: Check for two conditions (OR operator)
'''

class Database:

    @staticmethod
    def registerUser(user_obj):
        try:
            UsersCollection.insert_one(user_obj)
        
        except:
            return Database.insertionError()


    @staticmethod
    def registerMedia(media_obj):
        try:
            MediaCollection.insert_one(media_obj)
        
        except:
            return Database.insertionError()


    @staticmethod
    def registerReview(review_obj):
        try:
            ReviewsCollection.insert_one(review_obj)
        
        except:
            return Database.insertionError()
    

    @staticmethod
    def insertionError():
        print('Erro ao inserir objeto!\n')
        return False


    @staticmethod
    def searchUser(username=None, id=None): # Returns User dictionary
        try:
            if id:
                res = UsersCollection.find_one({'_id': ObjectId(id)})
                return res

            else:
                res = UsersCollection.find_one({'name': username})
                return res
        
        except:
            print('Erro ao buscar usuário!')
            return False


    @staticmethod
    def searchMedia(media_title=None, id=None): # Returns Media dictionary
        try:
            if id:
                res = MediaCollection.find_one({'_id': ObjectId(id)})
                return res

            else:
                res = MediaCollection.find_one({'title': media_title})
                return res
        
        except:
            print('Erro ao buscar obra!')
            return False


    @staticmethod
    def searchReview(review_comment=None, id=None, author_id=None): # return Media dictionary with review
        try:
            if id:
                res = ReviewsCollection.find_one({'_id': ObjectId(id)})

            elif author_id:
                res = ReviewsCollection.find_one({'author_id': author_id})

            else:
                res = ReviewsCollection.find_one({'text': review_comment})
            
            return res
        
        except:
            print('Erro ao buscar review!')
            return False
    

    @staticmethod
    def searchUserReviews(author_id=None, author_username=None):
        try:
            if author_id:
                res = list(ReviewsCollection.find({'author_id': author_id}))
                return res

            else:
                res = list(ReviewsCollection.find({'author_username': author_username}))
                return res

        except:
            print('Erro ao buscar review!')
            return False