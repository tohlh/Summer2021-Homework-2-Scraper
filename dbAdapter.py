import psycopg2
from psycopg2 import Error
import SECRETS

class adapter:
    connection = psycopg2.connect(user = SECRETS.db_username,
                              password = SECRETS.db_password,
                              host = SECRETS.db_address,
                              port = SECRETS.db_port,
                              database = SECRETS.db_name)

    cursor = connection.cursor()

    def connectDB(self):
        try:
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record)

        except (Exception, Error) as error:
            print('Unable to connect to database')

    def addChannelToQueue(self, id):
        # First, check if the channel is in the queue
        search_query = 'SELECT * FROM channelqueue WHERE id=\'{0}\';'.format(id)
        self.cursor.execute(search_query)
        result = self.cursor.fetchone()
        if result != None:
            return #already in queue
        # Second, if the channel is not in the queue
        insert_query = 'INSERT INTO channelqueue (id, scraped) values (\'{0}\', {1})'.format(id, False)
        self.cursor.execute(insert_query)
        self.connection.commit()

    def markChannelAsScraped(self, id):
        search_query = 'SELECT * FROM channelqueue WHERE id=\'{0}\';'.format(id)
        self.cursor.execute(search_query)
        result = self.cursor.fetchone()
        if result == None:
            return #does not exist
        update_query = 'UPDATE channelqueue SET scraped=True WHERE id=\'{0}\';'.format(id)
        self.cursor.execute(update_query)
        self.connection.commit()

    def getUnscrapedChannel(self):
        search_query = 'SELECT id FROM channelqueue WHERE scraped=False LIMIT 1;'
        self.cursor.execute(search_query)
        result = self.cursor.fetchone()
        if result == None:
            return ''
        return result[0]

    def saveChannelData(self, data):
        search_query = 'SELECT * FROM channels WHERE id=\'{0}\';'.format(id)
        result = self.cursor.fetchone()
        if result != None:
            return #already existed
        insert_query = '''INSERT INTO 
                        channels (id, name, profilepic, description, joineddate, totalviews, subscribercount, videos) 
                        values (%s, %s, %s, %s, %s, %s, %s, %s);'''
        self.cursor.execute(insert_query, (data['id'], data['name'], data['profilePic'], data['description'], data['joinedDate'], data['totalViews'], data['subscriberCount'], data['videos']))
        self.connection.commit()
        self.markChannelAsScraped(data['id'])     

    def getTotalChannelsToScrape(self):
        search_query = 'SELECT COUNT (*) FROM channelqueue'
        self.cursor.execute(search_query)
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def getScrapedChannelsNum(self):
        search_query = 'SELECT COUNT (*) FROM channelqueue WHERE scraped=true'
        self.cursor.execute(search_query)
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def addVideoToQueue(self, id):
        # First, check if the video is in the queue
        search_query = 'SELECT * FROM videoqueue WHERE id=\'{0}\';'.format(id)
        self.cursor.execute(search_query)
        result = self.cursor.fetchone()
        if result != None:
            return #already in queue
        # Second, if the video is not in the queue
        insert_query = 'INSERT INTO videoqueue (id, scraped) values (\'{0}\', {1})'.format(id, False) 
        self.cursor.execute(insert_query)
        self.connection.commit()

    def markVideoAsScraped(self, id):
        search_query = 'SELECT * FROM videoqueue WHERE id=\'{0}\';'.format(id)
        self.cursor.execute(search_query)
        result = self.cursor.fetchone()
        if result == None:
            return #does not exist
        update_query = 'UPDATE videoqueue SET scraped=True WHERE id=\'{0}\';'.format(id)
        self.cursor.execute(update_query)
        self.connection.commit()

    def getUnscrapedVideo(self):
        search_query = 'SELECT id FROM videoqueue WHERE scraped=False ORDER BY random() LIMIT 1;'
        self.cursor.execute(search_query)
        result = self.cursor.fetchone()
        if result == None:
            return ''
        return result[0]
    
    def saveVideoData(self, data):
        search_query = 'SELECT * FROM videos WHERE id=\'{0}\';'.format(id)
        result = self.cursor.fetchone()
        if result != None:
            return #already existed
        insert_query = '''INSERT INTO videos (id, title, description, videothumbnail, interactioncount, likecount, dislikecount, uploaddate, datepublished, channelid, genre, comments) 
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        self.cursor.execute(insert_query, (data['id'], data['title'], data['description'], data['videoThumbnail'], data['interactionCount'], data['likeCount'], data['dislikeCount'], data['uploadDate'], data['datePublished'], data['channelID'], data['genre'], data['comments']))
        self.connection.commit()
        self.markVideoAsScraped(data['id'])

    def getTotalVideosToScrape(self):
        search_query = 'SELECT COUNT (*) FROM videoqueue'
        self.cursor.execute(search_query)
        return self.cursor.fetchone()[0]

    def getScrapedVideosNum(self):
        search_query = 'SELECT COUNT (*) FROM videoqueue WHERE scraped=true'
        self.cursor.execute(search_query)
        self.connection.commit()
        return self.cursor.fetchone()[0]