import authentication as user_auth
import music_player as mp

class BeatBuddy:
    def __init__(self):
        pass

    def login_option(self):
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = None
        while not choice:
            choice = input("Enter you choice : ")
        choice = int(choice)
        obj_authentication = user_auth.authentication() #file object just to access the methods as it showsOOP
        match (choice):
            case 1:
                obj_authentication.login()
                self.option()
            case 2:
                obj_authentication.signup()
                self.option()
            case 3:
                exit()
            case _:
                print("!! Enter valid choice")

    def option(self):
        print(
            """
                 - - - - - - - - - - - - - - - - - - - - - - - - - -
                | W E L C O M E    T O    M U S I C    P L A Y E R  |
                 - - - - - - - - - - - - - - - - - - - - - - - - - -


1 - Create new playlist
2 - Play song from playlist
3 - Search song
4 - Edit playlist
5 - Display playlist
6 - To Exit The Application  """
        )
        choice = None 
        while not choice:
            choice = input("Enter you choice : ")
        choice = int(choice)
        musicplayer_obj=mp.music_player()
        match (choice):
            case 1:
                musicplayer_obj.create_playlist()
            case 2:
                musicplayer_obj.play_song_from_playlist()
            case 3:
                musicplayer_obj.search_music()
            case 4:
                musicplayer_obj.edit_paylist()
            case 5:
                musicplayer_obj.display_playlist()
            case 6:
                musicplayer_obj.upload_backup()
                print("Thank you for using our application! Have a nice day!")
                exit()
            case _:
                print("!! Enter valid choice")
        self.option()


obj = BeatBuddy()
obj.login_option()

###for calling all files
#starting file,main file
#all options available

#all methods used in class so imported