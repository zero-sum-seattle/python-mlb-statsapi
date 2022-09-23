class Sport: # Basic Sport Class
    id: int
    link: str
    abbreviation: str

    def __init__(self, id: int, link: str, abbreviation: str) -> None:
        self.id = id
        self.link = link
        self.abbreviation = abbreviation