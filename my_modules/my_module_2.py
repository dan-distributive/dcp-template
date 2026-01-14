# my_module_2.py

from .sub_modules import my_module_3

def some_other_function(x):
    """
    Delegates part of the computation to my_module_3.
    """
    return my_module_3.helper(x) * 2
