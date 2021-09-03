import time
import datetime as dt
from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import dbAdapter

da = dbAdapter.adapter()

videoData = {
    'id': '',
    'title': '',
    'description': '',
    'videoThumbnail': '',
    'interactionCount': 0,
    'likeCount': 0,
    'dislikeCount': 0,
    'uploadDate': dt.datetime(2021, 1, 1),
    'datePublished': dt.datetime(2021, 1, 1),
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
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Video info
        title = soup.find('meta', property='og:title')
        description = driver.find_element_by_xpath('//*[@id="description"]/yt-formatted-string').text
        videoThumbnail = soup.find('meta', property="og:image")
        interactionCount = soup.find('meta', itemprop='interactionCount')
        datePublished = soup.find('meta', itemprop='datePublished')
        genre = soup.find('meta', itemprop='genre')
        channelID = soup.find('meta', itemprop='channelId')

        videoData['id'] = id
        videoData['title'] = title['content']
        videoData['videoThumbnail'] = videoThumbnail['content']
        videoData['interactionCount'] = interactionCount['content']
        videoData['genre'] = genre['content']
        videoData['channelID'] = channelID['content']

        uploadDate_meta = soup.find('meta', itemprop='uploadDate')
        uploadDate = uploadDate_meta['content'].split('-')
        datePublished_meta = soup.find('meta', itemprop='uploadDate')
        datePublished = datePublished_meta['content'].split('-')
        videoData['uploadDate'] = dt.datetime(int(uploadDate[0]), int(uploadDate[1]), int(uploadDate[2]), tzinfo=timezone('Asia/Kuala_Lumpur'))
        videoData['datePublished'] = dt.datetime(int(datePublished[0]), int(datePublished[1]), int(datePublished[2]), tzinfo=timezone('Asia/Kuala_Lumpur'))

        likeCount = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string').get_attribute('aria-label')
        dislikeCount = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string').get_attribute('aria-label')
        
        if likeCount == None:
            likeCount = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string').text
        if dislikeCount == None:
            dislikeCount = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string').text
        
        videoData['likeCount'] = int(likeCount.replace(',', '').replace(' like', '').replace('s', '').replace('No', '0'))
        videoData['dislikeCount'] = int(dislikeCount.replace(',', '').replace(' dislike', '').replace('s', '').replace('No', '0'))

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

        driver.quit()
        da.saveVideoData(videoData)