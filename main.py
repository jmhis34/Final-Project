{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "import requests, json\n",
    "from splinter import Browser"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://www.fandango.com/90210_movietimes?mode=general&q=90210&date=2019-01-22\n"
     ]
    }
   ],
   "source": [
    "#https://www.fandango.com/44107_movietimes?mode=general&q=44107&date=2019-01-20\n",
    "zipcode = \"90210\"\n",
    "movie_date = \"2019-01-22\"\n",
    "url = (\"https://www.fandango.com/{0}_movietimes?mode=general&q={0}&date={1}\").format(zipcode, movie_date)\n",
    "print(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "executable_path = {'executable_path': 'static/webdriver/chromedriver'}\n",
    "browser = Browser('chrome', **executable_path, headless=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [],
   "source": [
    "browser.visit(url)\n",
    "# HTML object\n",
    "html = browser.html\n",
    "# Parse HTML with Beautiful Soup\n",
    "soup = BeautifulSoup(html, 'lxml')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "#page_response = requests.get(url, timeout=5)\n",
    "# here, we fetch the content from the url, using the requests library\n",
    "#soup = BeautifulSoup(page_response.content, \"lxml\")\n",
    "#we use the html parser to parse the url content and store it in a variable."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "showtimes = soup.find('div',class_='fd-showtimes')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "theaters = showtimes.find_all('li', class_='fd-theater')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [],
   "source": [
    "#create empty dictionary\n",
    "theater_data = []\n",
    "#Find theater_names, theater locations, movies, and showtimes.\n",
    "theater_names = []\n",
    "theater_locations = []\n",
    "theaters_movies = []\n",
    "for i in range(0,len(theaters)):\n",
    "    theater_name = theaters[i].find('a',class_='light').text\n",
    "    theater_names.append(theater_name)\n",
    "    theaterlocation = theaters[i].find('div',class_='fd-theater__address-wrap').text\n",
    "    theater_location = ' '.join(theaterlocation.rstrip().split())\n",
    "    theater_locations.append(theater_location)\n",
    "    movies = theaters[i].find_all('li',class_='fd-movie')\n",
    "    theater_movies = []\n",
    "    movies_titles = []\n",
    "    movies_showtimes = []\n",
    "    movies_posters = []\n",
    "    for k in range(0,len(movies)):\n",
    "        if movies[k].find('a',class_='dark'):\n",
    "            movie_title = movies[k].find('a',class_='dark').text\n",
    "        else:\n",
    "            movie_title = movies[k].find('a',class_='dark')\n",
    "        movies_titles.append(movie_title)\n",
    "        if movies[k].find('img'):\n",
    "            movie_poster = movies[k].find('img')['src']\n",
    "        else:\n",
    "            movie_poster = movies[k].find('img')\n",
    "        movies_posters.append(movie_poster)\n",
    "        movie_showtimes = []\n",
    "        numshows=movies[k].find_all('a',class_='showtime-btn--available')\n",
    "        for j in range(0,len(numshows)):\n",
    "            showtime = numshows[j].text\n",
    "            movie_showtimes.append(showtime)\n",
    "        movies_showtimes.append(movie_showtimes)\n",
    "        theater_movies.append({'Title':movies_titles[k],'Showtimes':movies_showtimes[k],'Poster_URL':movies_posters[k]})\n",
    "    theaters_movies.append(theater_movies)\n",
    "    theater_data.append({'Name':theater_names[i], 'Address':theater_locations[i],'Movies':theaters_movies[i]})"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "10"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(theaters_movies)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "10"
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "len(theater_data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[{'Title': 'Glass (2019)',\n",
       "  'Showtimes': ['2:00p', '5:00p', '8:15p'],\n",
       "  'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/213141/Glass.jpg'},\n",
       " {'Title': 'If Beale Street Could Talk',\n",
       "  'Showtimes': ['3:00p', '6:00p', '9:00p'],\n",
       "  'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/213339/IfBealeStreetCouldTalk2018.jpg'},\n",
       " {'Title': 'On the Basis of Sex',\n",
       "  'Showtimes': ['2:45p', '5:45p', '8:45p'],\n",
       "  'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/212847/OTBOS_Final_One%20Sheet.jpg'},\n",
       " {'Title': 'The Upside',\n",
       "  'Showtimes': ['2:15p', '5:15p', '8:30p'],\n",
       "  'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/214774/TheUpside2018.jpg'},\n",
       " {'Title': 'The Favourite',\n",
       "  'Showtimes': ['2:30p', '5:30p', '8:45p'],\n",
       "  'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/212924/TheFavourite2018.jpg'}]"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "theaters_movies[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'Glass (2019)'"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "theater_data[0]['Movies'][0]['Title']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'Name': 'AMC Sunset 5',\n",
       " 'Address': '8000 W. Sunset Blvd., Los Angeles, CA 90046',\n",
       " 'Movies': [{'Title': 'Glass (2019)',\n",
       "   'Showtimes': ['2:00p', '5:00p', '8:15p'],\n",
       "   'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/213141/Glass.jpg'},\n",
       "  {'Title': 'If Beale Street Could Talk',\n",
       "   'Showtimes': ['3:00p', '6:00p', '9:00p'],\n",
       "   'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/213339/IfBealeStreetCouldTalk2018.jpg'},\n",
       "  {'Title': 'On the Basis of Sex',\n",
       "   'Showtimes': ['2:45p', '5:45p', '8:45p'],\n",
       "   'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/212847/OTBOS_Final_One%20Sheet.jpg'},\n",
       "  {'Title': 'The Upside',\n",
       "   'Showtimes': ['2:15p', '5:15p', '8:30p'],\n",
       "   'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/214774/TheUpside2018.jpg'},\n",
       "  {'Title': 'The Favourite',\n",
       "   'Showtimes': ['2:30p', '5:30p', '8:45p'],\n",
       "   'Poster_URL': '//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/212924/TheFavourite2018.jpg'}]}"
      ]
     },
     "execution_count": 35,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "theater_data[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[\n",
      "    {\n",
      "        \"Address\": \"8000 W. Sunset Blvd., Los Angeles, CA 90046\",\n",
      "        \"Movies\": [\n",
      "            {\n",
      "                \"Poster_URL\": \"//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/213141/Glass.jpg\",\n",
      "                \"Showtimes\": [\n",
      "                    \"2:00p\",\n",
      "                    \"5:00p\",\n",
      "                    \"8:15p\"\n",
      "                ],\n",
      "                \"Title\": \"Glass (2019)\"\n",
      "            },\n",
      "            {\n",
      "                \"Poster_URL\": \"//images.fandango.com/ImageRenderer/200/0/redesign/static/img/default_poster.png/0/images/MasterRepository/fandango/213339/IfBealeStreetCouldTalk2018.jpg\",\n",
      "                \"Showtimes\": [\n",
      "                    \"3:00p\",\n",
      "                    \"6:00p\",\n",
      "                    \"9:00p\"\n",
      "                ],\n",
      "                \"Title\": \"If Beale Street Could Talk\"\n",
      "            },\n",
      "            {\n",
      "                \"Poster_URL\": \"//images.fandango.com/ImageRen...
