"""
Top Comment
2020
This program retrieves the highest voted comment from the top post of
the day and writes it to a file.
"""

from datetime import datetime as dt
import praw

CLIENT_ID = "XV-5vZD8mS9FDw"
CLIENT_SECRET = "SgeMB47tQ5ZD59VnQqmG7LnzcOQmEw"
USER_AGENT = "python:XV-5vZD8mS9FDw:v1.0 (by /u/PaperMech31)"
COMMENTS_FILE = "comments.txt"


def main():
    """Connect to Reddit API, then get top comment and write to file."""
    # Get current date.
    date_str = dt.now().strftime("%d/%m/%Y")
    # Check if comment has already been written.
    has_been_written = False
    with open(COMMENTS_FILE, "r") as file_in:
        for line in file_in:
            if line.startswith(date_str):
                has_been_written = True
    # If not, get comment and write to file.
    if not has_been_written:
        # Get top comment.
        top_comment = get_top_reddit_comment()
        with open(COMMENTS_FILE, "a") as file_out:
            file_out.write(date_str + " - ")
            file_out.write(top_comment + "\n")


def get_top_reddit_comment():
    """Connect to Reddit API and return the top comment of the top post."""
    # Connect to Reddit.
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )
    # Get top post.
    top_post = list(reddit.subreddit("all").top(limit=1, time_filter="day"))[0]
    # Get top comment.
    comment_scores = {c.score: c for c in top_post.comments[:-1]}
    top_comment = comment_scores[max(comment_scores)]
    return top_comment.body


if __name__ == '__main__':
    main()
