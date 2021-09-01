from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class creatorScraper:
    def scrapeCreator(self, baseUrl):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)

        # About page
        aboutUrl = baseUrl + '/about'
        driver.get(aboutUrl)
        profilePic = driver.find_element_by_xpath('//*[@id="img"]').get_attribute('src')
        description = driver.find_element_by_xpath('//*[@id="description"]').text
        joinedDate = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[2]/span[2]').text
        totalViews = driver.find_element_by_xpath('//*[@id="right-column"]/yt-formatted-string[3]').text
        subscribers = driver.find_element_by_xpath('//*[@id="subscriber-count"]').text
        print(profilePic)
        print(description)
        print(joinedDate)
        print(totalViews)
        print(subscribers)

        # Videos page
        videosUrl = baseUrl + '/videos'
        driver.get(videosUrl)
        videoLinksDump = open('./videoLinksDump.txt', 'w')
        videos = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
        for x in videos:
            if (str(x.get_attribute('href')) != 'None'):
                videoLinksDump.write(str(x.get_attribute('href')) + '\n')
