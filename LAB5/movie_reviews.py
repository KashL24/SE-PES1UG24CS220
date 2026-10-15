"""Manage movie ratings, reviews, rankings, and streaming information."""

import hashlib
import os
import secrets

STREAM_HOST = "127.0.0.1"
STREAM_PORT = 8000
MODERATOR_PASSWORD = os.getenv("MODERATOR_PASSWORD")
movies = {}


def add_movie(title, genre, year):
    """Add a movie to the collection."""
    movies[title] = {
        "genre": genre,
        "year": year,
        "ratings": [],
        "reviews": [],
    }


def rate_movie(title, stars, review_text=""):
    """Add a valid rating and an optional review to a movie."""
    if title not in movies:
        print(f"Movie not found: {title}")
        return False

    if not 1 <= stars <= 5:
        print(f"Rating must be between 1 and 5, got {stars}")
        return False

    movies[title]["ratings"].append(stars)

    if review_text:
        movies[title]["reviews"].append(review_text)

    return True


def average_rating(title):
    """Return a movie's average rating, or zero if it has no ratings."""
    movie = movies.get(title)

    if movie is None:
        return 0.0

    ratings = movie["ratings"]

    if not ratings:
        return 0.0

    return round(sum(ratings) / len(ratings), 1)


def top_movies(count=2):
    """Return the highest-rated movies."""
    ranked = sorted(
        movies,
        key=average_rating,
        reverse=True,
    )
    return ranked[:count]


def pick_featured():
    """Select a featured movie securely, or return None if none exist."""
    if not movies:
        return None

    return secrets.choice(sorted(movies))


def review_id(title, review_text):
    """Generate a shortened SHA-256 identifier for a review."""
    review_data = (title + review_text).encode("utf-8")
    return hashlib.sha256(review_data).hexdigest()[:10]


def print_all_reviews():
    """Print each movie and its average rating."""
    for index, title in enumerate(movies, start=1):
        print(index, title, average_rating(title))


def stream_address():
    """Return the streaming host and port."""
    return f"{STREAM_HOST}:{STREAM_PORT}"


def main():
    """Run a demonstration of the movie review system."""
    add_movie("The Long Road", "Drama", 2021)
    add_movie("Laugh Track", "Comedy", 2019)
    add_movie("Star Drift", "Sci-Fi", 2023)

    rate_movie("The Long Road", 5, "Beautiful story")
    rate_movie("The Long Road", 4, "A bit slow but worth it")
    rate_movie("Laugh Track", 2, "Not very funny")
    rate_movie("Star Drift", 6, "Out of range rating")
    rate_movie("Star Drift", 4)

    print_all_reviews()
    print("Top movies:", top_movies())
    print("Featured today:", pick_featured())
    print(
        "Review id:",
        review_id("Laugh Track", "Not very funny"),
    )
    print("Streaming from", stream_address())
    print(
        "Genres:",
        sorted(movie["genre"] for movie in movies.values()),
    )


if __name__ == "__main__":
    main()
