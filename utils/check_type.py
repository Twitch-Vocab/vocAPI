
#use a custom exception type, so these errors can be catched and treated differently than normal exceptions
#see message hub for handling of these errors
class BadTypeError(ValueError):
    '''raise when bad types happen'''
    
def assert_int(val, hint: str):
    type_name = type(val).__name__
    if type_name != "int":
        raise BadTypeError("Expected int, got " + type_name + " Hint: " + hint + ":" + str(val))

def assert_str(val, hint: str):
    type_name = type(val).__name__
    if type_name != "str":
        raise BadTypeError("Expected str, got " + type_name + " Hint: " + hint + ":" + str(val))

def assert_dict(val, hint: str):
    type_name = type(val).__name__
    if type_name != "dict":
        raise BadTypeError("Expected dict, got " + type_name + " Hint: " + hint + ":" + str(val))

def assert_list(val, hint: str):
    type_name = type(val).__name__
    if type_name != "list":
        raise BadTypeError("Expected list, got " + type_name + " Hint: " + hint + ":" + str(val))

def assert_bool(val, hint: str):
    type_name = type(val).__name__
    if type_name != "bool":
        raise BadTypeError("Expected bool, got " + type_name + " Hint: " + hint + ":" + str(val))


def get_mime(file_name:str):
    #make a copy with lower letters
    file_name_lower = file_name.lower()

    if file_name_lower.endswith('.jpg'):
        return "image/jpg"
    elif file_name_lower.endswith('.jpeg'):
        return "image/jpeg"
    elif file_name_lower.endswith('.png'):
        return "image/png"
    elif file_name_lower.endswith('.gif'):
        return "image/gif"
    elif file_name_lower.endswith('.pdf'):
        return "application/pdf"    
    elif file_name_lower.endswith('.txt'):
        return "text/plain"   
    elif file_name_lower.endswith('.mp3'):
        return "audio/mp3"         
    elif file_name_lower.endswith('.wav'):
        return "audio/wav"         
    elif file_name_lower.endswith('.mp4'):
        return "video/mp4"        
    elif file_name_lower.endswith('.json'):
        return "application/json"    
    elif file_name_lower.endswith('.html'):
        return "text/html"        
    elif file_name_lower.endswith('.js'):
        return "text/javascript"      
    elif file_name_lower.endswith('.css'):
        return "text/css"        

    return "application/octet-stream"  