import requests
import time
from bs4 import BeautifulSoup


def reptile_for_sina_blog(user_id, start_page, end_page, target_string, latency=0.1):
    base_url = "https://blog.sina.com.cn/s/articlelist_" + str(user_id) + "_0_PAGE.html"
    all_url = set()
    clean_url = set()

    for page in range(start_page, end_page + 1):
        url = base_url.replace("PAGE", str(page))
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href:
                    all_url.add(href)
        else:
            print(f"{response.status_code} for {url}")

        time.sleep(latency)

    for url in all_url:
        if url.startswith("//blog.sina.com.cn/s/blog_"):
            clean_url.add("https:" + url)

    with open('output.txt', 'w') as file:
        for url in clean_url:
            response = requests.get(url)

            if response.status_code == 200:
                print(f"{url}")
                soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')

                if target_string in str(soup):
                    file.write(f"{url}\n")
            else:
                print(f"{response.status_code} for {url}")

            time.sleep(latency)
