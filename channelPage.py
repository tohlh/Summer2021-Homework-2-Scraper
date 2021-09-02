import datetime as dt
from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import dbAdapter

da = dbAdapter.adapter()

months = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    "Jul": 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

channelData = {
    'id': '',
    'name': '',
    'profilePic': '',
    'description': '',
    'joinedDate': dt.datetime(2021, 1, 1),
    'totalViews': '',
    'subscriberCount': '',
    'videos': []
}

class channelScraper:
    def scrapeChannel(self, id):
        baseUrl = 'https://www.youtube.com/channel/{0}'.format(id)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)

        # About page
        aboutUrl = baseUrl + '/about'
        driver.get(aboutUrl)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        channelData['id'] = id
        channelData['name'] = driver.find_element_by_xpath('//*[@id="channel-name"]').text
        channelData['profilePic'] = driver.find_element_by_xpath('//*[@id="img"]').get_attribute('src')
        channelData['description'] = driver.find_element_by_xpath('//*[@id="description"]').text

        totalViews = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[3]').text
        subscriberCount = driver.find_element_by_xpath('//*[@id="subscriber-count"]').text
        channelData['totalViews'] = int(totalViews[0:-6].replace(',', ''))
        channelData['subscriberCount'] = subscriberCount.replace(' subscribers', '')

        joinedDate = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[2]/span[2]').text
        dateTime = joinedDate.replace(',', '').split(' ')
        channelData['joinedDate'] = dt.datetime(int(dateTime[2]), months[dateTime[0]], int(dateTime[1]), tzinfo=timezone('Asia/Kuala_Lumpur'))

        # Videos page
        i = 0
        videosUrl = baseUrl + '/videos'
        driver.get(videosUrl)
        videoLinksDump = open('./videoLinksDump.txt', 'w')
        videos = driver.find_elements_by_xpath('//*[@id="video-title"]')
        for x in videos:
            if (x.get_attribute('href') != None):
                videoID = str(x.get_attribute('href')).replace('https://www.youtube.com/watch?v=', '')
                channelData['videos'].append(videoID)
                da.addVideoToQueue(videoID)
                i += 1
                if i >= 20:
                    break

        da.saveChannelData(channelData)