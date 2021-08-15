from model.Exceptions import NamespaceError


def stripEachItem(lst):
    for i in range(0, len(lst)):
        lst[i] = lst[i].strip()  # get rid of spaces attached to parameters from splicing


def assertExistNamespace(memory):
    try:
        memory.currentNamespace
    except: #what error?
        raise NamespaceError("no current namespace is set")

