

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import stripe
from collections import defaultdict

# ================= DS IMPORTS =================
from ds.models import Movie
from ds.linkedlist import LinkedList
from ds.stack import Stack
from ds.queue import Queue
from ds.bst import BST
from ds.show_graph import ShowGraph

# ================= APP SETUP =================
app = Flask(__name__)
app.secret_key = "dev-secret-key"

PRICE_PER_SEAT = 150
ADULT_PRICE = 150
KID_PRICE = 100

# ================= STRIPE =================
import os

STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY


# ================= MOVIES =================
NORMAL_MOVIES = {
    "Samraat Prithviraj": "https://images.filmibeat.com/img/2022/05/prithh-1652100562.jpg",
    "Bajirao Mastani": "https://images004-a.media.erosnow.com/movie/4/1023354/img625352/6785378/1023354_6785378_43.jpg",
    "Jodha Akbar": "https://static.digit.in/OTT/v2/images/jodhaa-akbar-32952jpg",
    "Shivaay": "https://2.bp.blogspot.com/-RW_USDVQkbs/V6dDcjbqzYI/AAAAAAAAbm4/KI3kht4nrywd-fbdI8MHRWtHg1d1AzOJACLcB/s1600/shivaay.jpg",
    "Natsamraat": "https://cdn2.marathistars.com/wp-content/uploads/2015/11/Natsamrat-Marathi-Movie.jpg",
    "Chhava": "https://indian.community/wp-content/uploads/2025/01/chhava-1024x576.png",
    "Duniyadari": "https://img1.hotstarext.com/image/upload/f_auto/sources/r1/cms/prod/1636/1720471671636-h",
    "Bajrangi Bhaijaan": "https://images.plex.tv/photo?size=large-1280&url=https:%2F%2Fmetadata-static.plex.tv%2F6%2Fgracenote%2F6b530651a9439f7833ab9a99f50edbee.jpg",
    "Drishyam": "https://tse3.mm.bing.net/th/id/OIP.VjcTkHI2_qfrEk0SOYv3mgHaEo?w=800&h=500&rs=1&pid=ImgDetMain&o=7&rm=3",
    "Padmaavat": "https://wallpapercave.com/wp/wp2380454.jpg",
    "Raam Leela": "https://static.digit.in/OTT/v2/images/optimised/goliyon-ki-raasleela-ram-leela-1236018.webp",
    "3 Idiots": "https://cfm.yidio.com/images/movie/33070/backdrop-1280x720.jpg"
}

KIDS_MOVIES = {
    "Finding Nemo": "https://images5.alphacoders.com/133/thumb-1920-1337263.png",
    "Toy Story": "https://wallpaperaccess.com/full/3678373.jpg",
    "The Lion King": "https://ntvb.tmsimg.com/assets/p14113286_v_h10_af.jpg?w=960&h=540",
    "Kung Fu Panda": "https://wallpaperaccess.com/full/10868904.jpg",
    "Frozen": "https://tse2.mm.bing.net/th/id/OIP.WXe3iA4p7Su6fRovj2qr7QHaEK?rs=1&pid=ImgDetMain&o=7&rm=3",
    "Minions": "https://images.hdqwalls.com/download/minions-movie-1920x1080.jpg",
    "Cars": "https://4kwallpapers.com/images/walls/thumbs_2t/18082.jpg",
    "Up": "https://cdn.wallpapersafari.com/94/62/olhnCi.jpg"
}

MOVIES = []
MOVIE_BST = BST()

# Normal movies
for i, (title, img) in enumerate(NORMAL_MOVIES.items()):
    movie = Movie(i, title, 8, 10, img, "normal")
    MOVIES.append(movie)
    MOVIE_BST.insert(title.lower(), movie)

# Kids movies
start_id = len(MOVIES)
for j, (title, img) in enumerate(KIDS_MOVIES.items()):
    movie = Movie(start_id + j, title, 6, 8, img, "kids")
    MOVIES.append(movie)
    MOVIE_BST.insert(title.lower(), movie)

# ================= SHOWS =================
ALL_SHOWS = [
    # ================= KIDS MOVIES SHOWS =================
# Dedicated Kids Screens: Screen 4, 5, 6

    # Finding Nemo
    ("Finding Nemo", "10AM", "Screen 4"),
    ("Finding Nemo", "1PM", "Screen 5"),
    ("Finding Nemo", "4PM", "Screen 6"),
    ("Finding Nemo", "7PM", "Screen 4"),

    # Toy Story
    ("Toy Story", "10AM", "Screen 5"),
    ("Toy Story", "1PM", "Screen 6"),
    ("Toy Story", "4PM", "Screen 4"),
    ("Toy Story", "7PM", "Screen 5"),

    # The Lion King
    ("The Lion King", "10AM", "Screen 6"),
    ("The Lion King", "1PM", "Screen 4"),
    ("The Lion King", "4PM", "Screen 5"),
    ("The Lion King", "7PM", "Screen 6"),

    # Kung Fu Panda
    ("Kung Fu Panda", "10AM", "Screen 4"),
    ("Kung Fu Panda", "1PM", "Screen 5"),
    ("Kung Fu Panda", "4PM", "Screen 6"),
    ("Kung Fu Panda", "7PM", "Screen 4"),

    # Frozen
    ("Frozen", "10AM", "Screen 5"),
    ("Frozen", "1PM", "Screen 6"),
    ("Frozen", "4PM", "Screen 4"),
    ("Frozen", "7PM", "Screen 5"),

    # Minions
    ("Minions", "10AM", "Screen 6"),
    ("Minions", "1PM", "Screen 4"),
    ("Minions", "4PM", "Screen 5"),
    ("Minions", "7PM", "Screen 6"),

    # Cars
    ("Cars", "10AM", "Screen 4"),
    ("Cars", "1PM", "Screen 5"),
    ("Cars", "4PM", "Screen 6"),
    ("Cars", "7PM", "Screen 4"),

    # Up
    ("Up", "10AM", "Screen 5"),
    ("Up", "1PM", "Screen 6"),
    ("Up", "4PM", "Screen 4"),
    ("Up", "7PM", "Screen 5"),

    # Samraat Prithviraj
    ("Samraat Prithviraj", "11AM", "Screen 1"),
    ("Samraat Prithviraj", "2:30PM", "Screen 2"),
    ("Samraat Prithviraj", "6PM", "Screen 3"),
    ("Samraat Prithviraj", "9:30PM", "Screen 1"),

    # Bajirao Mastani
    ("Bajirao Mastani", "11AM", "Screen 2"),
    ("Bajirao Mastani", "2:30PM", "Screen 3"),
    ("Bajirao Mastani", "6PM", "Screen 1"),
    ("Bajirao Mastani", "9:30PM", "Screen 2"),

    # Jodha Akbar
    ("Jodha Akbar", "11AM", "Screen 3"),
    ("Jodha Akbar", "2:30PM", "Screen 1"),
    ("Jodha Akbar", "6PM", "Screen 2"),
    ("Jodha Akbar", "9:30PM", "Screen 3"),

    # Shivaay
    ("Shivaay", "11AM", "Screen 1"),
    ("Shivaay", "2:30PM", "Screen 2"),
    ("Shivaay", "6PM", "Screen 3"),
    ("Shivaay", "9:30PM", "Screen 1"),

    # Natsamraat
    ("Natsamraat", "11AM", "Screen 2"),
    ("Natsamraat", "2:30PM", "Screen 3"),
    ("Natsamraat", "6PM", "Screen 1"),
    ("Natsamraat", "9:30PM", "Screen 2"),

    # Chhava
    ("Chhava", "11AM", "Screen 3"),
    ("Chhava", "2:30PM", "Screen 1"),
    ("Chhava", "6PM", "Screen 2"),
    ("Chhava", "9:30PM", "Screen 3"),

    # Duniyadari
    ("Duniyadari", "11AM", "Screen 1"),
    ("Duniyadari", "2:30PM", "Screen 2"),
    ("Duniyadari", "6PM", "Screen 3"),
    ("Duniyadari", "9:30PM", "Screen 1"),

    # Bajrangi Bhaijaan
    ("Bajrangi Bhaijaan", "11AM", "Screen 2"),
    ("Bajrangi Bhaijaan", "2:30PM", "Screen 3"),
    ("Bajrangi Bhaijaan", "6PM", "Screen 1"),
    ("Bajrangi Bhaijaan", "9:30PM", "Screen 2"),

    # Drishyam
    ("Drishyam", "11AM", "Screen 3"),
    ("Drishyam", "2:30PM", "Screen 1"),
    ("Drishyam", "6PM", "Screen 2"),
    ("Drishyam", "9:30PM", "Screen 3"),

    # Padmaavat
    ("Padmaavat", "11AM", "Screen 1"),
    ("Padmaavat", "2:30PM", "Screen 2"),
    ("Padmaavat", "6PM", "Screen 3"),
    ("Padmaavat", "9:30PM", "Screen 1"),

    # Raam Leela
    ("Raam Leela", "11AM", "Screen 2"),
    ("Raam Leela", "2:30PM", "Screen 3"),
    ("Raam Leela", "6PM", "Screen 1"),
    ("Raam Leela", "9:30PM", "Screen 2"),

    # 3 Idiots
    ("3 Idiots", "11AM", "Screen 3"),
    ("3 Idiots", "2:30PM", "Screen 1"),
    ("3 Idiots", "6PM", "Screen 2"),
    ("3 Idiots", "9:30PM", "Screen 3"),
]

SHOW_GRAPH = ShowGraph()
movie_to_shows = defaultdict(list)

for movie, time, screen in ALL_SHOWS:
    show_id = f"{movie}_{time}"
    SHOW_GRAPH.add_show(show_id, movie, time, screen)
    movie_to_shows[movie].append(show_id)

for shows in movie_to_shows.values():
    for i in range(len(shows) - 1):
        SHOW_GRAPH.add_edge(shows[i], shows[i + 1])

# ================= STATE =================
state = {
    "seat_manager": LinkedList(),
    "undo_stack": Stack(),
    "selected_show": None
}

BOOKING_QUEUE = Queue()

# ================= ROUTES =================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/movies")
def movies():
    return render_template("movies.html", movies=MOVIES)

@app.route("/kids")
def kids_movies():
    kids = [m for m in MOVIES if m.category == "kids"]
    return render_template("movies.html", movies=kids, title="Kids Movies")

@app.route("/search")
def search():
    q = request.args.get("q", "").strip().lower()
    if not q:
        return redirect(url_for("movies"))

    result = MOVIE_BST.search(q)
    if result:
        return render_template("movies.html", movies=[result])

    flash("Movie not found")
    return redirect(url_for("movies"))

@app.route("/shows/<int:movie_id>")
def shows(movie_id):
    movie = next((m for m in MOVIES if m.id == movie_id), None)
    if not movie:
        return redirect(url_for("movies"))

    show_ids = SHOW_GRAPH.get_shows_for_movie(movie.title)
    shows = [{"id": sid, **SHOW_GRAPH.get_show(sid)} for sid in show_ids]

    return render_template("shows.html", movie=movie, shows=shows)

@app.route("/ticket_type/<show_id>", methods=["GET", "POST"])
def ticket_type(show_id):
    show = SHOW_GRAPH.get_show(show_id)
    movie = next(m for m in MOVIES if m.title == show["movie"])

    if movie.category != "kids":
        return redirect(url_for("select_seats", show_id=show_id))

    if request.method == "POST":
        adults = int(request.form["adults"])
        kids = int(request.form["kids"])

        if adults < 1:
            flash("At least one adult required")
            return redirect(request.url)

        state["adults"] = adults
        state["kids"] = kids
        return redirect(url_for("select_seats", show_id=show_id))

    return render_template("ticket_type.html", movie=movie, show=show)

@app.route("/seats/<show_id>")
def select_seats(show_id):
    state["selected_show"] = show_id

    show = SHOW_GRAPH.get_show(show_id)
    movie = next(m for m in MOVIES if m.title == show["movie"])
    
    for r in range(movie.rows):
        for c in range(movie.cols):
            movie.seats[r][c] = False

    # ✅ Mark already booked seats (INSIDE FUNCTION)
    for seat in show["booked_seats"]:
        row = ord(seat[0]) - 65
        col = int(seat[1:]) - 1
        movie.seats[row][col] = True

    # ✅ Now outside the loop but still inside function
    selected = state["seat_manager"].to_list()

    if movie.category == "kids":
        total = (
            state.get("adults", 0) * ADULT_PRICE +
            state.get("kids", 0) * KID_PRICE
        )
    else:
        total = len(selected) * PRICE_PER_SEAT

    return render_template(
        "seats.html",
        movie=movie,
        time=show["time"],
        screen=show["screen"],
        selected=selected,
        total=total,
        price_per_seat=PRICE_PER_SEAT,
        ADULT_PRICE=ADULT_PRICE,
        KID_PRICE=KID_PRICE,
        state=state
    )

@app.route("/toggle_seats", methods=["POST"])
def toggle_seats():
    seats = request.form.getlist("seat")
    state["seat_manager"].clear()
    state["undo_stack"] = Stack()

    for s in seats:
        state["seat_manager"].add(s)
        state["undo_stack"].push(s)

    return redirect(url_for("select_seats", show_id=state["selected_show"]))

@app.route("/undo", methods=["POST"])
def undo():
    if not state["undo_stack"].is_empty():
        last = state["undo_stack"].pop()
        state["seat_manager"].remove(last)

    return redirect(url_for("select_seats", show_id=state["selected_show"]))

@app.route("/checkout")
def checkout():
    selected = state["seat_manager"].to_list()
    show_id = state.get("selected_show")

    if not selected or not show_id:
        return redirect(url_for("movies"))

    show = SHOW_GRAPH.get_show(show_id)
    movie = next(m for m in MOVIES if m.title == show["movie"])

    if movie.category == "kids":
        total = state.get("adults", 0) * ADULT_PRICE + state.get("kids", 0) * KID_PRICE
    else:
        total = len(selected) * PRICE_PER_SEAT

    intent = stripe.PaymentIntent.create(
        amount=total * 100,
        currency="inr"
    )

    return render_template(
        "checkout.html",
        total=total,
        movie=show["movie"],
        time=show["time"],
        screen=show["screen"],
        stripe_public_key=STRIPE_PUBLIC_KEY,
        client_secret=intent.client_secret
    )

@app.route("/confirm_booking", methods=["POST"])
def confirm_booking():

    show_id = state.get("selected_show")

    if not show_id:
        return {"status": "error"}, 400

    # Get show & movie
    show = SHOW_GRAPH.get_show(show_id)
    movie = next(m for m in MOVIES if m.title == show["movie"])

    # Get selected seats
    seats = state["seat_manager"].to_list()

    # ✅ SAVE SEATS TO SHOW (IMPORTANT)
    for seat in seats:
        show["booked_seats"].add(seat)

    # Calculate total
    if movie.category == "kids":
        total = (
            state.get("adults", 0) * ADULT_PRICE +
            state.get("kids", 0) * KID_PRICE
        )
    else:
        total = len(seats) * PRICE_PER_SEAT

    # Save history
    BOOKING_QUEUE.enqueue({
        "movie": show["movie"],
        "time": show["time"],
        "screen": show["screen"],
        "seats": ", ".join(seats),
        "amount": total,
        "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
    })

    # ✅ RESET STATE SAFELY
    state["seat_manager"] = LinkedList()
    state["undo_stack"] = Stack()
    state["selected_show"] = None
    state.pop("adults", None)
    state.pop("kids", None)

    return {"status": "success"}

@app.route("/history")
def history():
    return render_template("history.html", history=BOOKING_QUEUE.to_list())

if __name__ == "__main__":
    app.run(debug=True)
