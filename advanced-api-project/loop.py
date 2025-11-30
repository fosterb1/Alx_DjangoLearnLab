def infinite_gen():
    i = 0
    while True:
        yield i

# This will run indefinitely
for num in infinite_gen():
    print(num)