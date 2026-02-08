class ShowGraph:
    def __init__(self):
        self.graph = {}
        self.show_info = {}  # show_id → details

    def add_show(self, show_id, movie, time, screen):
        self.graph[show_id] = []
        self.show_info[show_id] = {
            "movie": movie,
            "time": time,
            "screen": screen,
            "booked_seats": set()
        }

    def add_edge(self, from_show, to_show):
        self.graph[from_show].append(to_show)

    def get_shows_for_movie(self, movie):
        return [
            sid for sid, info in self.show_info.items()
            if info["movie"] == movie
        ]

    def get_show(self, show_id):
        return self.show_info[show_id]
