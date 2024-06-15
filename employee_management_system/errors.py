class MandatoryInputMissingException(Exception):
    def __init___(self, message):
        super(MandatoryInputMissingException, self).__init__(message)
        self.message = message

class CharacterLengthException(Exception):
    def __init___(self, message):
        super(CharacterLengthException, self).__init__(message)
        self.message = message
        
class OperationalException(Exception):
    def __init__(self,message):
        super(OperationalException,self).__init__(message)
        self.message = message
        
class PhoneEmailExistsException(Exception):
    def __init___(self, message):
        super(PhoneEmailExistsException, self).__init__(message)
        self.message = message
        
class InvalidPhoneEmailFormat(Exception):
    def __init___(self, message):
        super(InvalidPhoneEmailFormat, self).__init__(message)
        self.message = message
        
class UserNotExistsException(Exception):
    def __init___(self, message):
        super(UserNotExistsException, self).__init__(message)
        self.message = message
        
class InvalidCredentialException(Exception):
    def __init___(self, message):
        super(InvalidCredentialException, self).__init__(message)
        self.message = message
class UserNotAuthorized(Exception):
    def __init___(self, message):
        super(UserNotAuthorized, self).__init__(message)
        self.message = message