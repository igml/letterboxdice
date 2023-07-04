"""
Description: This program will pick a random film for you to watch after being provided a Letterboxd List.
Date: July 1st, 2023
"""

from bs4 import BeautifulSoup
import requests
import random

def main(saved_url):

    if saved_url == '':
  
      print('This will choose a random movie for you to watch!')
  
      base_url = 'https://letterboxd.com/tobiasandersen2/list/random-movie-roulette/'
  
      prompt = True
      while prompt:
        url = input('\nPlease input a Letterboxd List, or leave this field blank and press enter: ').lower()
  
        if url == '':
          start = 8
          url = base_url
          prompt = False
          continue
  
        # If the provided website does not end with a forward slash, we will add it to the url now.
  
        elif url[len(url) - 1] != '/':
          url += '/'
  
        idx = 0
  
        letterboxd = False
        catalog = False
  
        for char in url:
          if char == 'l':
            if url[idx:idx + 14] == 'letterboxd.com':
              start = idx
              letterboxd = True
  
          elif char == '/':
            if url[idx:idx + 6] == '/list/':
                catalog = True
  
          if letterboxd and catalog:
            prompt = False
            break
  
          idx += 1
  
        error = '\n'
        if letterboxd and not catalog:
          error += 'URL must be a List.'
  
        elif (not letterboxd and catalog) or (not letterboxd and not catalog):
          error += 'URL must be Letterboxd.'
  
        error += ' Please try again.'
  
        if prompt == True:
          print(error)
      # If the url is in the form letterboxd.com without https://, this will add it so that BeautifulSoup will avoid an error.
  
      if start == 0:
        url = 'https://' + url
  
      # Remove /page/# extension from URL if provided.
  
      idx = 0
      for char in url:
        if char == '/':
          if url[idx:idx + 6] == '/page/':
            url = url[0:idx + 1]
            break
            
        idx += 1
    else:
      url = saved_url

      

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    html = soup.findAll('li', attrs={'class':'paginate-page'})

    if html == []:
      print('\nThe link you entered was an invalid Letterboxd List. Please run the program again.')
      return None

    # Gets the last page number of the Letterboxd List.

    last_line = html[len(html) - 1]

    last_page = int(last_line.text)

    # Make a backup of our original url for later use.
  
    old_url = url

    # Re-uses previous variables to build and visit the last page of the provided Letterboxd List.
    # We will now use this to retrieve the total number of films in the List.

    url = url + 'page/' + str(last_page) + '/'
  
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    html = soup.findAll('li', attrs={'class':'poster-container'})

    num_films = (last_page - 1) * 100 + len(html)

    chosen_film = random.randint(1, num_films)

    landing_page = chosen_film // 100 + 1

    print(f'\nFilms to Choose From: {num_films}\n\nNavigate to Page: {landing_page}\nFilm Number: #{chosen_film}\n')

    url = old_url + 'page/' + str(landing_page) + '/'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    html = soup.findAll('li', attrs={'class':'poster-container'})

    selected_lines = str(html[chosen_film - 1 - (100 * (landing_page - 1))])

    # This will retrieve and build the film link.

    film_url = 'https://letterboxd.com'

    num_quotes = 0
    found = False

    idx = 0

    for char in selected_lines:
      if char == 'd' and not found:
        if selected_lines[idx:idx + 14] == 'data-film-slug':
          found = True

      elif found and char == '"':
        num_quotes += 1
        if num_quotes == 2:
          break

      elif num_quotes == 1:
        film_url += char
        
      idx += 1

    print(f'Film Link: {film_url}\n')

    response = requests.get(film_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    html = soup.find('title')

    title = html.text

    film_info = ''
    for char in title:
      if char == '•':
        break
      film_info += char

    print(f'Your chosen film is: {film_info}\n')

    return old_url

# The user can choose to request another film recommendation as many times as they want from the same list as before.
# This is where main is called.

url = ''

repeat = True
while repeat:
  url = main(url)

  if url == None:
    repeat = False
    continue

  prompt = True

  while prompt:
    user_input = input('Roll again? (Y/N) ').lower()
  
    if user_input == 'yes' or user_input == 'y':
      prompt = False
  
    elif user_input == 'no' or user_input == 'n':
      repeat = False
      prompt = False
      break
  
    else:
      print('\nInvalid Input.\n')
