
for i, threshold in enumerate([1, 2, 3, 4, 5]):
    print(i, threshold)

# expalin enumerate
# enumerate is a built-in function of Python. It allows us to loop over something and have an automatic counter. Here is an example:
#explain the output
# The enumerate object yields pairs containing a count (from start, which defaults to zero) and a value yielded by the iterable argument.
for threshold in enumerate([1, 2, 3, 4, 5]):
    print(threshold)