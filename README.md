# Summer2021-Homework-2-Scraper

## 2021 夏季学期 - 大作业（二）- 第一部分 - 爬虫

大作业[第二部分](https://github.com/tohlh/Summer2021-Homework-2-Site)

## 所使用的工具/技术
BeautifulSoup4、Selenium、Psycopg2、PostgreSQL

## 算法实现
首先在PostgreSQL中创建4个表：`channelqueue`、`channels`、`videoqueue`、`videos`

### 第一阶段

爬虫程序会先从 YouTube 主页爬取所显示的视频中各作者ID。程序中可以预设欲爬取的作者信息数量。作业要求了至少要爬取250个作者和5000个视频，意味着250个作者中，每个作者要爬取至少20个视频。考虑到有些作者可能上传的视频少于20个，因此我预设了在此阶段爬取至少300个作者，确保之后爬取的视频数量能达标。

在 YouTube 频道主页的链接有以下 3 种:

```
www.youtube.com/c/<Channel Name>

www.youtube.com/channel/<ID>

www.youtube.com/user/<ID>
```

程序只会爬取第一种链接的频道，因为能有这种 URL 的作者都有：1）订阅人数至少有100个、2）已上传头像、3）已上传背景图像、4）至少创建了30天。因此，这些频道的资料会比较齐全。

第一阶段阶段所爬取的所有影片会被记录在 `channelqueue` 中，当中有两个列：`id`（作者的ID）和 `scraped` (爬取了没，会先记为 `False`)。

### 第二阶段

找到了300个作者后，程序将开始爬取每个作者的信息。程序会随机爬去 `channelqueue` 中 `scraped = False` 的作者，并储存该作者信息在 `channels` 中。设为随机的目的在于给多个进程分配不同的作者ID，使它们能同时爬取多个作者，大大提高爬取的速度。使用云端上的数据库甚至能在多台电脑中执行多个进程。

其中最重要的是爬取每个作者所上传的视频ID，并放入 `videoqueue` 中。爬取了的作者将在 `channelqueue` 中标记 `scraped = True`，避免程序重新爬去该作者。

### 第三阶段

最后一个阶段是随机爬取 `videoqueue` 中 `scraped = False` 的视频，并储存在 `videos` 中。此阶段和第二阶段类似。

## 所爬取数据

去除了一些不合适的作者之后，我最终得到了 **297个作者** 和 **5859个视频**。
