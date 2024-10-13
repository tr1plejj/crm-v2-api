# from functools import wraps
#
#
# def inner_dec(arg):
#     def dec(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             print('before', arg)
#             res = func(*args, **kwargs)
#             print(res)
#             print('after', arg-1)
#         return wrapper
#     return dec
#
# @inner_dec(1)
# def print_hello(title):
#     return f'hello {title}'
#
# # know = inner_dec('hello')(print_hello('oleg'))
# # funcs = know.__name__
# # print(funcs)
# print_hello('oleg')