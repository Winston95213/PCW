from random import random


# A list of ten people name
names = ["John", "Paul", "George", "Ringo", "Pete", "Stuart", "Mick", "Keith", "Ronnie", "Charlie"]


# A function that could be used to generate a random number
def random_number() -> int:
    return random.randint(0, 100)


#tower of Hanoi
def tower_of_hanoi(n, source, destination, auxiliary):
    if n == 1:
        print("Move disk 1 from source", source, "to destination", destination)
        return
    tower_of_hanoi(n - 1, source, auxiliary, destination)
    print("Move disk", n, "from source", source, "to destination", destination)
    tower_of_hanoi(n - 1, auxiliary, destination, source)


