class Foo () :
    bar = 1

    def __init__ (self) :
        self.baz = Foo.bar
    
    def increment (self) :
        Foo.bar += 1
        self.baz = Foo.bar

class Faa () :
    bar = 1

    @classmethod
    def increase_bar (cls) :
        cls.bar += 1

    def __init__ (self) :
        self.baz = Faa.bar
    
    def increment (self) :
        Faa.increase_bar()
        self.baz = Faa.bar

foo_1 = Foo()

print("foo_1 baz " + str(foo_1.baz)) # 1

print()

foo_1.increment() 
print("increment foo_1")
foo_2 = Foo()

print()

print("foo_1 baz " + str(foo_1.baz)) # 2
print("foo_2 baz " + str(foo_2.baz)) # 2

print()
print()
print()

faa_1 = Faa()

print("faa_1 baz " + str(faa_1.baz)) # 1

print()

faa_1.increment()
print("increment faa_1")
faa_2 = Faa()

print()

print("faa_1 baz " + str(faa_1.baz)) # 2
print("faa_2 baz " + str(faa_2.baz)) # 2

print()
print()
print()