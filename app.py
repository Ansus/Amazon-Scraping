from bs4 import BeautifulSoup
import requests
import pandas as pd

# taking the list of movies from IMdb.com
url = "https://www.imdb.com/list/ls021348496/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

css_selector = ".lister-item-content"
items = soup.select(css_selector)

rows_list = []
for item in items:
    header = item.select_one(".lister-item-header").getText().splitlines()
    rank, title, year = header[1:4]
    rank = "".join(c for c in rank if c.isdigit())
    year = "".join(c for c in year if c.isdigit())

    runtime = item.select_one(".runtime").getText()
    runtime = "".join(c for c in runtime if c.isdigit())

    genre = item.select_one(".genre").getText()
    genre_list = [x.strip() for x in genre.split(",")]

    rating = item.select_one(".ipl-rating-star__rating").getText()

    # distiguish the revenue from votes (same structure)
    chars = ["$", "€"]
    num_revenue, num_votes = None, None
    for my_tag in item.find_all(attrs={"name": "nv"}):
        text = my_tag.getText()
        digits = "".join(c for c in text if c.isdigit())
        if any(x in text for x in chars):
            num_revenue = float(digits)/100
        else:
            num_votes = int(digits)

    row = {
        "Rank": int(rank),
        "Title": title,
        "Year": int(year),
        "Minutes": runtime,
        "Genre1": genre_list[0] if len(genre_list) > 0 else None,
        "Genre2": genre_list[1] if len(genre_list) > 1 else None,
        "Genre3": genre_list[2] if len(genre_list) > 2 else None,
        "Rating": float(rating),
        "Votes": num_votes,
        "Revenue": num_revenue
    }
    rows_list.append(row)
df = pd.DataFrame(rows_list)
print(df["Votes"])
