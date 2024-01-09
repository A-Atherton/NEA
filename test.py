import os

def load_levels():
    with os.scandir("levels/") as entries:
        for enty in entries:
            level_layout = []
            with open(enty, "r") as level:
                for line in level:
                    level_layout.append(line)
            print(level_layout)