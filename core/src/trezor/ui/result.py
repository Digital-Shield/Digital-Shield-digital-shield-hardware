class Result:
    def __init__(self, value):
        self.value = value


class NavigationBack:
    """"
    Navigation screen navigate back
    """
    def __bool__(self):
        return False

class Redo:
    """
    Some operation need redo
    """

class AutoClose:
    """"
    Modeled screen auto close
    """

    def __bool__(self):
        return False

class Done:
    def __bool__(self):
        return True

class Confirm:
    def __bool__(self):
        return True

class Reject:
    def __bool__(self):
        return False

class Cancel:
    def __bool__(self):
        return False

class Continue:
    def __bool__(self):
        return True

class More:
    def __bool__(self):
        return True

class Detail:
    def __bool__(self):
        return True
