import dbAdapter
import mainPage
import channelPage
import videoPage

da = dbAdapter.adapter()
ms = mainPage.mainPageScraper()
cs = channelPage.channelScraper()
vs = videoPage.videoScraper()

# Configuration
channelsToScrape = 10
videosToScrape = 5000

def main():
    print("Starting to scrape main page for channel links...")
    totalChannelLinks = da.getTotalChannelsToScrape()
    while (totalChannelLinks < channelsToScrape):
        ms.scrapeMainPage(channelsToScrape)
        totalChannelLinks = da.getTotalChannelsToScrape()
    print("Found {0} unique channels!".format(totalChannelLinks))
    
    currChannel = da.getUnscrapedChannel()
    while currChannel != '':
        print('Scraping channel ID: {0}...'.format(currChannel))
        cs.scrapeChannel(currChannel)
        currChannel = da.getUnscrapedChannel()
        print('Done!')

    currVideo = da.getUnscrapedVideo()
    while currVideo != '':
        print('Scraping video ID: {0}...'.format(currVideo))
        vs.scrapeVideo(currVideo)
        currVideo = da.getUnscrapedVideo()
        print('Done!')

if __name__ == "__main__":
    main()