import os


with os.scandir('levels/') as entries:
    for entry in entries:
        level_layout = []
        with open(entry, 'r') as level:
            for line in level:
                level_layout.append(line.rstrip("\n"))
        print(level_layout)
