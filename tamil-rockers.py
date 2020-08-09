import argparse
from bs4 import BeautifulSoup
import re
import requests

BASE_URL = 'https://tamilrockers.ws/index.php/forum/115-tamil-new-dvdrips-hdrips-bdrips-movies/page-{}?prune_day=100&sort_by=Z-A&sort_key=last_post&topicfilter=all'

def get_movies_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='forum_table')

    movies_list = []

    movies = results.find_all('tr', class_='__topic')
    for movie in movies:
        content = movie.find('td', class_='col_f_content')
        title = content.find('a', class_='topic_title')
        movie_dict = {}
        movie_dict['title'] = title.text.strip()
        movie_dict['movie_url'] = title['href']

        movies_list.append(movie_dict)
    return movies_list

def search_movie(movies_list, key):
    entries = []
    for movie in movies_list:
        if re.search(key.strip().lower(), movie['title'].strip().lower()):
            entries.append(movie)
    return entries

def view_movie(movie):
    print(movie['title'])
    print(movie['movie_url'])

def show_movies(movies_list):
    for movie in movies_list:
        view_movie(movie)
        print()

if __name__ == "__main__":
    cmd_parser = argparse.ArgumentParser(
                description="Tamilrockers movie searcher", 
                epilog='Enjoy the movie'
            )

    cmd_parser.add_argument(
                    '-m', 
                    metavar='movie', 
                    type=str, 
                    help='movie name to be searched',
                    required=False
                )

    args = cmd_parser.parse_args()

    print(args.m)

    found = False
    i=1
    while not found:
        URL = BASE_URL.format(i)
        print("Searching page : {}".format(i))
        movies_list = get_movies_list(URL)
        if args.m:
            movies_list = search_movie(movies_list, args.m)
        if movies_list:
            show_movies(movies_list)
        print()
        i += 1