from models import (
    User
)

class Validate:
    get_result= User.select()

    def password(self,username,password):
        
        get_password = User.select().where(User.username == username)
        if password == get_password:
            return True
        return False
            
    def username(self ,*args , **kwargs):

        for i in self.get_result:
            if i.username == args:
                return False
        return True
        
    def email(self , *args , **kwargs):

        for i in self.get_result:
            if i.email == args:
                return False
        return True
        
    
            

