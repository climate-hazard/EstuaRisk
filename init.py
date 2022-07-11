class Estuary:
    def __init__(self, name, description, location, items):
        self.name = name
        self.description = description
        self.location = location
        self.items = items


if __name__ == '__main__':
    from . import main
    main.main()
