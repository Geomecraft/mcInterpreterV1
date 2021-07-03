def stripEachItem(lst):
    for i in range(0, len(lst)):
        lst[i] = lst[i].strip()  # get rid of spaces attached to parameters from splicing