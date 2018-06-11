class Vehicle:
    Country = 'China'

    def __init__(self, name, speed, load, power):
        self.name = name
        self.speed = speed
        self.load = load
        self.power = power

    def run(self):
        print('发动啦')


class Subway(Vehicle):
    def __init__(self, name, speed, load, power, line):
        super(Subway, self).__init__(name, speed, load, power)
        self.line = line

    def show_info(self):
        print(self.name, self.line)

    def run(self):
        super(Subway, self).run()
        print('%s %s开动啦' % (self.name, self.line))


line13 = Subway('北京地铁', '70km/h', '600', '电', '13line')

line13.show_info()
line13.run()
