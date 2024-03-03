import os

def load_levels():
    with os.scandir("game_files/levels/") as entries:
        for entry in entries:
            level_layout = []
            with open(entry, "r") as level:
                for line in level:
                    level_layout.append(line)
            print(level_layout)

load_levels()