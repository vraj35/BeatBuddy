import pygame

class MusicPlayer:
    def __init__(self, playlist):
        pygame.init()
        pygame.mixer.init() #mixer module
        self.playlist = playlist
        self.current_index = 0
        self.play(0)

    def play(self, index):
        print("-------------------- Play")
        try:
            if 0 <= index < len(self.playlist):
                pygame.mixer.music.load(self.playlist[index])
                pygame.mixer.music.play()
                self.current_index = index
        except pygame.error as e:
            print("Pygame error:", e)

    def stop(self):
        print("-------------------- stop")
        self.current_index = 0
        pygame.mixer.music.stop()

    def play_next(self):
        print("-------------------- playnext")
        next_index = (self.current_index + 1) % len(self.playlist) #looping will go to last song then will return to the 1st one
        self.stop()
        self.play(next_index)

    def play_previous(self):
        print("-------------------- playprev")
        previous_index = (self.current_index - 1) % len(self.playlist)
        self.stop()
        self.play(previous_index)

    def operation_choice(self):
        print("-------------------- choice")
        print("Options:")
        print("1. Play")
        print("2. Next")
        print("3. Previous")
        print("4. Stop")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print(self.current_index)
            self.play(self.current_index)
        elif choice == "2":
            self.play_next()
        elif choice == "3":
            self.play_previous()
        elif choice == "4":
            self.stop()
        elif choice == "5":
            self.stop()
            return
        else:
            print("Invalid choice. Please try again.")
        self.operation_choice()