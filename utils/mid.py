import random
import time

from typing import Text


valid_characters = "0123456789abcdefghijklmnopqrstuvwxyz"


class MID:

    def __init__(self, str: Text = ""):
        self.valid = True
        self.empty = False

        if not str:
            str = ""

        if len(str) != 32:
            self.valid = False

        for c in str:
            if c not in valid_characters: 
                self.valid = False

        if self.valid:
            self.str = str
        else:
            self.valid = True
            self.str = "0000000000000000000000000000000"
            self.empty = True

    @staticmethod
    def rand():
        str = "%x" % int(time.time())

        for i in range(0, 24):
            str = str + valid_characters[random.randint(0, len(valid_characters)-1)]

        return MID(str)
