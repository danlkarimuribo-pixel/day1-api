class NoteNotFoundError(Exception):
    def __init__(self, note_id: int):
        self.note_id = note_id
