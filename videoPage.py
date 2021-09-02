import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

videoData = {
    'id': '',
    'title': '',
    'description': '',
    'videoThumbnail': '',
    'interactionCount': 0,
    'uploadDate': '',
    'datePublished': '',
    'channelID': '',
    'genre': '',
    'comments': []
}

class videoScraper:
    def scrapeVideo(self, id):
        baseUrl = 'https://www.youtube.com/watch?v=' + id
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        driver.get(baseUrl)
        driver.execute_script('window.scrollTo(1, 500);')
        time.sleep(2)
        driver.execute_script('window.scrollTo(1, 10000);')
        
        # Video info
        videoData['id'] = id
        videoData['title'] = driver.find_element_by_xpath('//*[@id="watch7-content"]/meta[1]').get_attribute('content')
        videoData['videoThumbnail'] = driver.find_element_by_xpath('//*[@id="watch7-content"]/link[2]').get_attribute('content')
        videoData['interactionCount'] = driver.find_element_by_xpath('//*[@id="watch7-content"]/meta[13]').get_attribute('content')
        videoData['uploadDate'] = driver.find_element_by_xpath('//*[@id="watch7-content"]/meta[15]').get_attribute('content')
        videoData['datePublished'] = driver.find_element_by_xpath('//*[@id="watch7-content"]/meta[14]').get_attribute('content')
        videoData['genre'] = driver.find_element_by_xpath('//*[@id="watch7-content"]/meta[16]').get_attribute('content')
        videoData['channelID'] = driver.find_element_by_xpath('//*[@id="watch7-content"]/meta[4]').get_attribute('content')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        description_div = soup.find('div', {'id': 'description', 'slot': 'content', 'class': 'style-scope ytd-video-secondary-info-renderer'})
        description_formatted = description_div.find('yt-formatted-string')
        videoData['description'] = description_formatted.get_text()

        # Comments
        driver.execute_script('window.scrollTo(1, 20000);')
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        commentThreads = soup.findAll('ytd-comment-thread-renderer', limit=5)
        for x in commentThreads:
            commentContents = x.find('yt-formatted-string', {'class': 'style-scope ytd-comment-renderer', 'id': 'content-text'})
            videoData['comments'].append(commentContents.get_text())

        # Related videos
        videoLinksDump = open('videoLinksDump.txt', 'w')
        videos = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
        for x in videos:
            if (str(x.get_attribute('href')) != 'None'):
                videoLinksDump.write(str(x.get_attribute('href')) + '\n')