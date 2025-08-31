import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def setup(driver_path):
    try:
        # Using ChromeDriver service i
        cService = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=cService)  
        return driver
    except Exception as e:
        print(f"Something went wrong: {e}")
        return None  # Return None if WebDriver setup fails

def scrape_imdb_top_movies(driver_path, total_movies):
    website = "https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_special,video,tv_series,tv_miniseries&interests=in0000186&sort=num_votes,desc"
    
    driver = setup(driver_path)
    if driver is None:
        return []

    def _click_50_more_until_enough():
    
        while True:
            #selecting main container
            containers = driver.find_elements(By.XPATH, '//div[@class="ipc-metadata-list-summary-item__tc"]')
            if len(containers) >= total_movies:
                break
            try:
                # Scroll to bottom so the button is in view
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.8)

                # find and click the '50 more'  button to load more movies
                load_more = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[contains(@class,"ipc-see-more__text")]'))
                )
                prev = len(containers)
                try:
                    load_more.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", load_more)

                # Wait until more items actually appear
                WebDriverWait(driver, 12).until(
                    lambda d: len(d.find_elements(By.XPATH, '//div[@class="ipc-metadata-list-summary-item__tc"]')) > prev
                )
                time.sleep(0.8)  # small settle
            except Exception:
                print("No more '50 more' button or cannot load more.")
                break

    try: 
        driver.get(website)  
        #creating dictionary to store data
        row_dict = {
            'rank': np.nan,
            'title': np.nan,
            'release_year': np.nan,
            'duration': np.nan,
            'rate_type': np.nan,
            'star_rating': np.nan,
            'rated_by': np.nan,
            'genre': np.nan,
            'Main Cast': np.nan,
            'Box Office Revenue' : np.nan,
            'directors': np.nan,
            'reviews': np.nan,
            'user review num': np.nan,
        }

        data = []
        movie_links = []

        _click_50_more_until_enough()

        #  first `total_movies` containers
        containers = driver.find_elements(By.XPATH, '//div[@class="ipc-metadata-list-summary-item__tc"]')[:total_movies]

        # Collect metadata of movies + links of individual movies 
        for container in containers:
            row = row_dict.copy()
            try:
                row['rank'], row['title'] = container.find_element(By.CLASS_NAME, 'ipc-title__text').text.split('.')
            except Exception as e:
                print(f"Error extracting rank and title: {e}")

            try:
                movie_metadata_container = container.find_element(By.XPATH, './/div[@class="sc-15ac7568-6 fqJJPW dli-title-metadata"]')
                try:
                    metadata = movie_metadata_container.find_elements(By.XPATH, './span[@class="sc-15ac7568-7 cCsint dli-title-metadata-item"]')
                    row['release_year'] = metadata[0].text if len(metadata) > 0 else np.nan
                    row['duration'] = metadata[1].text if len(metadata) > 1 else np.nan
                    row['rate_type'] = metadata[2].text if len(metadata) > 2 else np.nan
                except Exception as e:
                    print(f"Error extracting metadata: {e}")
            except Exception as e:
                print(f"Error extracting metadata container: {e}")

            try:
                row['star_rating'] = container.find_element(By.XPATH, './/span[@class="ipc-rating-star--rating"]').text
            except Exception as e:
                print(f"Error extracting star rating: {e}")
            try:
                row['rated_by'] = container.find_element(By.XPATH, './/span[@class="ipc-rating-star--voteCount"]').text
            except Exception as e:
                print(f"Error extracting rated by: {e}")

            # Link
            try:
                movie_link = container.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").get_attribute('href')
                movie_links.append((row, movie_link))
            except Exception as e:
                print(f"Error extracting movie link: {e}")
                continue

            data.append(row)

        # Visit each movie page for details + reviews
        for i, (row, link) in enumerate(movie_links):
            try:
                print(f"Navigating to movie page: {link}")
                driver.get(link)

                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="ipc-page-content-container ipc-page-content-container--full sc-8b4a7eec-0 loYWEn"]')
                ))
                time.sleep(2)

                containers2 = driver.find_elements(By.XPATH, '//div[@class="ipc-page-content-container ipc-page-content-container--full sc-8b4a7eec-0 loYWEn"]')
                for container2 in containers2:
                    try:
                        genre_container = container2.find_elements(By.XPATH, '//span[@class="ipc-chip__text"]')
                        row['genre'] = [el.text for el in genre_container]
                    except Exception as e:
                        print(f"Error extracting genre: {e}")
                    try:
                        maincast_container = container2.find_elements(By.XPATH, './/div[@class="sc-10bde568-5 dWhYSc"]')
                        row['Main Cast'] = [el.text.split("\n")[0] for el in maincast_container]
                    except Exception as e:
                        print(f"Error extracting maincast: {e}")
                    try:
                        box_container = container2.find_elements(By.XPATH, './/div[@data-testid="title-boxoffice-section"]')
                        row['Box Office Revenue'] = [el.text for el in box_container]
                    except Exception as e:
                        print(f"Error extracting revenue: {e}")
                    try:
                        row['directors'] = container2.find_element(By.XPATH, './/div[@class="ipc-metadata-list-item__content-container"]').text
                    except Exception as e:
                        print(f"Error extracting directors: {e}")

                # Reviews sections
                try:
                    review_link = driver.find_element(By.LINK_TEXT, "User reviews")
                    review_link.click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, './/article[@class="sc-12fe603f-1 dHhKiF user-review-item"]')
                    ))
                    time.sleep(2)
                except Exception as e:
                    print(f"Error clicking on the reviews link: {e}")

                containers3 = driver.find_elements(By.XPATH, './/article[contains(@class,"user-review-item")]')
                cleaned_reviews = []
                for art in containers3:
                    raw = art.text
                    main = re.split(r'\bHelpful\b', raw, maxsplit=1)[0].strip()
                    lines = [ln.strip() for ln in main.split('\n') if ln.strip()]

                    rating = None
                    title = None
                    body = None
                    if len(lines) >= 3 and lines[1] == '/10' and lines[0].isdigit():
                        rating = int(lines[0])
                        title = lines[2]
                        body  = ' '.join(lines[3:]).strip() if len(lines) > 3 else ''
                    else:
                        title = lines[0] if lines else ''
                        body  = ' '.join(lines[1:]).strip() if len(lines) > 1 else ''
                    cleaned_reviews.append({'rating': rating, 'title': title, 'body': body})

                row['reviews'] = cleaned_reviews

                try:
                    row['user review num'] = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tturv-total-reviews"]').text
                except Exception as e:
                    print(f"Error extracting total reviews: {e}")

            except Exception as e:
                print(f"Error extracting movie data for {link}: {e}")

        return data

    except Exception as e:
        print(f"Error during scraping: {e}")
        return [] 
    finally:
        driver.quit()


def main(data):
    if data:
        df = pd.DataFrame(data)
        df.to_csv('movie data.csv', index=False)
    else:
        print("No data to save.")

data = scrape_imdb_top_movies("/Users/afsanarubyat/Downloads/chromedriver-mac-arm64 2/chromedriver", 250)
main(data)