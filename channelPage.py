from selenium import webdriver
from selenium.webdriver.chrome.options import Options

channelData = {
    'id': '',
    'name': '',
    'profilePic': '',
    'description': '',
    'joinedDate': '',
    'totalViews': '',
    'subscriberCount': '',
    'videos': []
}

class channelScraper:
    def scrapeChannel(self, baseUrl):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)

        # About page
        aboutUrl = baseUrl + '/about'
        driver.get(aboutUrl)
        channelData['id'] = driver.find_element_by_xpath('/html/body/meta[47]').get_attribute('content')
        channelData['name'] = driver.find_element_by_xpath('//*[@id="channel-name"]').text
        channelData['profilePic'] = driver.find_element_by_xpath('//*[@id="img"]').get_attribute('src')
        channelData['description'] = driver.find_element_by_xpath('//*[@id="description"]').text
        channelData['joinedDate'] = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[2]/span[2]').text
        totalViews = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[3]').text
        channelData['totalViews'] = int(totalViews[0:-6].replace(',', ''))
        subscriberCount = driver.find_element_by_xpath('//*[@id="subscriber-count"]').text
        channelData['subscriberCount'] = subscriberCount.replace(' subscribers', '')

        # Videos page
        videosUrl = baseUrl + '/videos'
        driver.get(videosUrl)
        videoLinksDump = open('./videoLinksDump.txt', 'w')
        videos = driver.find_elements_by_xpath('//*[@id="video-title"]')
        for x in videos:
            if (x.get_attribute('href') != None):
                channelData['videos'].append(str(x.get_attribute('href')).replace('https://www.youtube.com/watch?v=', ''))

        tempDump = open('tempDump.txt', 'w')
        tempDump.write(str(channelData))

