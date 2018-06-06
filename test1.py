class Animal(object):
    def __init__(self, name):
        self.name = name

    def greet(self):
        print('hello,%s' % self.name)


class Dog(Animal):
    def greet(self):
        super().greet()
        print("wangwang ")


dog = Dog('小白')

dog.greet()
