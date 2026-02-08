class Movie:
    def __init__(self, id, title, rows, cols, image, category="normal"):
        self.id = id
        self.title = title
        self.rows = rows
        self.cols = cols
        self.image = image
        self.category = category
        self.seats = [[False for _ in range(cols)] for _ in range(rows)]

        
        #self.seats = [[False for _ in range(cols)] for _ in range(rows)]

    def total_seats(self):
        return self.rows * self.cols
    
    def available_seats_count(self):
        booked = 0
        for row in self.seats:
         for seat in row:
            if seat:
                booked += 1
        return self.rows * self.cols - booked

    def seat_label(self, r, c):
        # Seat label e.g., A1, A2 ... B1 ...
        return f"{chr(65 + r)}{c+1}"

    def is_booked(self, r, c):
        return self.seats[r][c]

    def book(self, r, c):
        if not self.seats[r][c]:
            self.seats[r][c] = True
            return True
        return False
