""""
README
======
This file contains Python codes.
======
"""

class Greeting(object):
    def __init__(self, my_greeting):
        self.my_greeting = my_greeting

    def say_hello(self, name):
        print("%s %s" % (self.my_greeting, name))

greeting = Greeting("Hello")
greeting.say_hello("World")
greeting.say_hello("Dog")
greeting.say_hello("Cat")
