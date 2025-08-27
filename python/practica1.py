'''
An isogram is a word that has no repeating letters, consecutive or non-consecutive. 
Implement a function that determines whether a string that contains only letters is an isogram. 
Assume the empty string is an isogram. Ignore letter case.
'''

def is_isogram(string):
    for i in string.lower():
        if string.count(i) > 1 or string != "":
            return False
        else:
            return True