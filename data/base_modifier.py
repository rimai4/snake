class BaseModifier:
    def set_icon_location(self):
        raise NotImplementedError

    def hide(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def modify(self):
        pass

    def reset(self):
        pass
