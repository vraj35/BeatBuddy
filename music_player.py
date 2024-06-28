import mysql.connector
import os
import shutil
import operation as o
import random


class music_player:
    def __init__(self):
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="beatbuddy",
            autocommit=True,
        )
        self.mycursor = self.con.cursor()

    def create_playlist(self):
        playlist_name = input("Enter playlist name : ")
        os.mkdir("D:\\beatbuddy\\" + playlist_name)  #mkdir-create folder
        os.mkdir("D:\\beatbuddy\\" + playlist_name + "\\data")
        f = open("D:\\beatbuddy\\" + playlist_name + "\\data\\custom_sequance.txt", "w")
        f.close()
        f = open(
            "D:\\beatbuddy\\" + playlist_name + "\\data\\current_sequance.txt", "w"
        )
        f.close()
        print("Playlist succssfully created")

    def play_song_from_playlist(self):
        list_of_playlists = os.listdir("D:\\beatbuddy") #which playlist? will give list
        for i in range(len(list_of_playlists)):
            print(f"({i+3}) {list_of_playlists[i]}") #{i+1}-1 index starting from 0
        play_choice = int(input("Enter Playlist id which you want to play : "))
        playlist_name = list_of_playlists[play_choice - 1] 
        f = open(
            "D:\\beatbuddy\\" + playlist_name + "\\data\\current_sequance.txt", "r"
        )
        playlist = f.read().split("\n")# line by line read
        f.close()
        path = "D:\\beatbuddy\\" + playlist_name + "\\"
        playlist = [path + song for song in playlist]
        self.o = o.MusicPlayer(playlist)  #operation class's obj
        self.o.operation_choice()

    def edit_paylist(self):
        list_of_playlists = os.listdir("D:\\beatbuddy")
        for i in range(len(list_of_playlists)):
            print(f"({i+1}) {list_of_playlists[i]}")
        playlist_choice = int(input("Enter Playlist id which you want to edit : "))
        playlist_name = list_of_playlists[playlist_choice - 1]
        list_of_songs = os.listdir("D:\\beatbuddy\\" + playlist_name)
        list_of_songs.remove("data")
        print("1. Sort by Title")
        print("2. Shuffle playlsit")
        print("3. Custom order")
       
        edit_choice = int(input("Enter Selected option : "))
        match (edit_choice):
            case 1:
                list_of_songs.sort()
                self.update_edited_data(playlist_name, list_of_songs)
                return
            case 2:
                random.shuffle(list_of_songs)
                self.update_edited_data(playlist_name, list_of_songs)
                return
            case 3:
                f = open(
                    "D:\\beatbuddy\\" + playlist_name + "\\data\\custom_sequance.txt"
                )
                custom_list_of_songs = f.read().split("\n")
                f.close()
                self.update_edited_data(playlist_name, custom_list_of_songs)
                return
            
            case _:
                print("Select valid option !!")
        self.edit_paylist()

    def update_edited_data(self, playlist_name, list_of_songs):
        f = open(
            "D:\\beatbuddy\\" + playlist_name + "\\data\\current_sequance.txt", "w"
        )
        for song in list_of_songs:
            f.write(song + "\n")
        f.close()

    def display_playlist(self):
        f = open("playlist.txt", "w")
        list_of_playlist = os.listdir("D:\\beatbuddy")
        for playlist in list_of_playlist:
            f.write(
                "----------------------------------------------------------------\n"
            )
            f.write("Playlist name : " + playlist + "\n")
            f.write("Songs : \n")
            list_of_songs = os.listdir("D:\\beatbuddy\\" + playlist)
            for song in list_of_songs:
                if os.path.isfile("D:\\beatbuddy\\" + playlist + "\\" + song):
                    song = song[: song.rfind(".")] # slicing from 0th index to .  raney.mp3--raney
                    f.write("  -> " + song + "\n")
            f.write("\n")
        f.close()
        os.startfile("playlist.txt")

    def search_music(self):
        print(
            "----------------------------------------------------------------------"
        )
        search_result1 = []
        search_result2 = []
        search_result3 = []
        final_result = []
        search_song = input("Enter song name : ")
        query = "Select song_name from songs "
        self.mycursor.execute(query)
        server_songs = self.mycursor.fetchall()
        for song in server_songs:
            if song[0].startswith(search_song):
                search_result1.append(song[0])
            elif song[0].__contains__(search_song):
                search_result2.append(song[0])
            elif song[0].endswith(search_song):
                search_result3.append(song[0])
        final_result.extend(search_result1)
        final_result.extend(search_result2)
        final_result.extend(search_result3)
        if len(final_result) == 0:
            print("No result found !!")
            return
        for i in range(len(final_result)):
            print(f"({i+1}) {final_result[i]}")
        print()
        song_choice = int(input("Choice : "))
        song_name = final_result[song_choice - 1]
        print(
            """----------------------------------------------------------------------
1. want to add in playlist
2. Want to play the song
"""
        )
        choice = int(input("Choice :"))
        match (choice):
            case 1:
                list_of_playlist = os.listdir("D:\\beatbuddy")
                for i, j in enumerate(list_of_playlist):
                    print(f"({i+1}) {j}")
                playlist_choice = int(
                    input("select playlist : ")
                )
                playlist_name = list_of_playlist[playlist_choice - 1]
                self.add_song(playlist_name, song_name)
            case 2:
                f = open(song_name + ".mp3", "wb")
                f.write(self.fatch_song_data(song_name))
                f.close()
                self.o = o.MusicPlayer([song_name + ".mp3"])
                self.o.operation_choice()

    def add_song(self, playlist_name, song_name):
        query = "Select song_data from songs where song_name = %s"
        val = (song_name,)
        self.mycursor.execute(query, val)
        content = self.mycursor.fetchone()[0]
        f = open("D:\\beatbuddy\\" + playlist_name + "\\" + song_name + ".mp3", "wb")
        f.write(content)
        f.close()
        f = open(
            "D:\\beatbuddy\\" + playlist_name + "\\data\\current_sequance.txt", "a"
        )
        f.write(song_name + ".mp3\n")
        f.close()
        f = open("D:\\beatbuddy\\" + playlist_name + "\\data\\custom_sequance.txt", "a")
        f.write(song_name + ".mp3\n")
        f.close()

    def fatch_song_data(self, song_name):
        query = "Select song_data from songs where song_name=%s"
        val = (song_name,)
        self.mycursor.execute(query, val)
        data = self.mycursor.fetchone()[0]
        return data



   