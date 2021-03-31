class Room(object):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.encounter = None

rooms = {
    'basic': [
        Room('Room A', 'Beautifully poetic description of a room within the mine. Poetic language abounds. Metaphors! Similes! You weep with sexy admiration.'),
        Room('Room B', 'Poorly written description of a room within the mine. Needs to be improved. You are uninspired by this room, sadly.'),
    ],
}
