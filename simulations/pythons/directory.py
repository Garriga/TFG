import os
def check(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.mkdir(directory)
