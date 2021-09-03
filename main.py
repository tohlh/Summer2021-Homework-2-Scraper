import dbAdapter
import mainPage
import channelPage
import videoPage

da = dbAdapter.adapter()
ms = mainPage.mainPageScraper()

# Configuration
channelsToScrape = 300

def main():
    print("Starting to scrape main page for channel links...")
    totalChannelLinks = da.getTotalChannelsToScrape()
    while (totalChannelLinks < channelsToScrape):
        ms.scrapeMainPage(channelsToScrape)
        totalChannelLinks = da.getTotalChannelsToScrape()
    print("Found {0} unique channels!".format(totalChannelLinks))
    
    currChannel = da.getUnscrapedChannel()
    while currChannel != '':
        print('Scraping channel ID: {0} ({1}/{2})'.format(currChannel, da.getScrapedChannelsNum() + 1, da.getTotalChannelsToScrape()))
        cs = channelPage.channelScraper()
        cs.scrapeChannel(currChannel)
        currChannel = da.getUnscrapedChannel()
        print('Done!')
    print('Finished scrapping {0} channels!'.format(da.getScrapedChannelsNum()))

    currVideo = da.getUnscrapedVideo()
    while currVideo != '':
        print('Scraping video ID: {0} ({1}/{2})'.format(currVideo, da.getScrapedVideosNum() + 1, da.getTotalVideosToScrape()))
        vs = videoPage.videoScraper()
        vs.scrapeVideo(currVideo)
        currVideo = da.getUnscrapedVideo()
        print('Done!')
    print('Finished scrapping {0} videos!'.format(da.getScrapedVideosNum()))

if __name__ == "__main__":
    main()