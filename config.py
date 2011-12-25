import ConfigParser
import getpass

def ask_for_input(prompt, default=None):
    if default != None:
        prompt = prompt + " [" + str(default) + "]"
            
        if isinstance(default, str):
            cast_func = str
            
        elif isinstance(default, int):
            cast_func = int
            
        else:
            cast_func = str
        
    
    r = raw_input(prompt)
    if r == '' and default != None:
        r = default
    else:
        r = cast_func(r)
    
    return r

def ask_for_login():
    username = raw_input('Your vkontakte.ru login: ')
    password = getpass.getpass('Your vkontakte.ru password:')
    save_password = ask_for_input('Save password (y/n)?', default = 'y')
    
    if save_password == 'y':
        config = ConfigParser.ConfigParser()
        config.add_section('login details')
        config.set('login details', 'username', username)
        config.set('login details', 'password', password)
        config.write(open('config.ini', 'w'));
        
    return (username, password)

if __name__ == "__main__":
    main()