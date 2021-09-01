import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class videoScraper:
    def scrapeVideo(self, baseUrl):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        driver.get(baseUrl)
        driver.execute_script('window.scrollTo(1, 500);')
        time.sleep(1)
        driver.execute_script('window.scrollTo(1, 10000);')
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Video info
        title = soup.find('meta', property='og:title')
        image = soup.find('meta', property="og:image")
        url = soup.find('meta', property='og:url')
        videoUrl = soup.find('meta', property='og:video:url')
        interactionCount = soup.find('meta', itemprop='interactionCount')
        uploadDate = soup.find('meta', itemprop='uploadDate')
        datePublished = soup.find('meta', itemprop='datePublished')
        genre = soup.find('meta', itemprop='genre')

        description_div = soup.find('div', {'id': 'description'})
        description_formatted = description_div.find('yt-formatted-string')
        description = description_formatted.get_text()

        print(title['content'])
        print(description)
        print(image['content'])
        print(url['content'])
        print(videoUrl['content'])
        print(interactionCount['content'])
        print(uploadDate['content'])
        print(datePublished['content'])
        print(genre['content'])

        # Creator info
        author = soup.find('span', itemprop='author')
        authorUrl = author.find('link', itemprop='url')
        authorName = author.find('link', itemprop='name')
        print(authorUrl['href'])
        print(authorName['content'])

        # Related videos
        videoLinksDump = open('videoLinksDump.txt', 'w')
        videos = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
        for x in videos:
            if (str(x.get_attribute('href')) != 'None'):
                videoLinksDump.write(str(x.get_attribute('href')) + '\n')

        # Comments
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentThreads = soup.findAll('ytd-comment-thread-renderer', limit=5)
        comments = []
        for x in commentThreads:
            commentContents = x.find('yt-formatted-string', {'class': 'style-scope ytd-comment-renderer', 'id': 'content-text'})
            comment = commentContents.get_text()
            comments.append(comment)
            print(comment + '\n')
