class RBCat:
    def __init__(self, cats_id: int | None = None,
                 age: int | None = None,
                 breed: str | None = None,
                 color: str | None = None,
                 description: str | None = None):
        self.id = cats_id
        self.age = age
        self.breed = breed
        self.color = color
        self.description = description

    def to_dict(self) -> dict:
        data = {'id': self.id, 'age': self.age, 'breed': self.breed, 'color': self.color,
                'description': self.description}
        # копия словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is
                         not None}
        return filtered_data
