# -*- coding: utf-8 -*-

import os
import string
import json
from pprint import pprint

from scrapy import signals
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.xlib.pydispatch import dispatcher


valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
save_filename = lambda filename: ''.join([c for c in filename if c in valid_chars])


class VideoSpider(CrawlSpider):
    name = 'videos'
    start_urls = ['http://unity3d.com/learn/tutorials/modules/beginner']

    def __init__(self):
        self.topics = []
        os.system('mkdir -p /tmp/videos')
        os.system('mkdir videos')
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def parse(self, response):
        
        sel = Selector(response)
        cur_level_idx = -1
        cur_topic_idx = -1
        cur_topic = None
        cur_topic_path = None
        g12n_lst = sel.css('.g12n')
        
        for g12n in g12n_lst:
            # Header
            if g12n.css('.g12n.mb10'):
                title = g12n.css('.pa20 h1.mb0').xpath('text()').extract()[0]
                descr = g12n.css('.pt10.mb0').xpath('text()').extract()[0]
                cur_topic = {
                    'title': title.strip(),
                    'descr': descr.strip(),
                    'levels': [],
                }
                cur_topic_path = os.path.join('videos', save_filename(cur_topic['title'])).replace(' ', '_')
                cur_level_idx = -1
                cur_topic_idx += 1
                self.topics.append(cur_topic)
            # Section blocks                
            elif g12n.css('.g12n.mb20'): 
                title = g12n.css('.g12 h4').xpath('text()').extract()[0]
                cur_level = {
                    'title': title.strip(),
                    'videos': [],
                }
                cur_path = os.path.join(cur_topic_path, cur_level['title']).replace(' ', '_')
                cmd = 'mkdir -p %s' % cur_path
                self.log('Level.CMD: %s' % cmd)
                os.system(cmd)
                cur_level_idx += 1
                cur_topic['levels'].append(cur_level)
                # One section
                for number, item in enumerate(g12n.css('.g4.mb0 p.mb0 a'), 1):
                    url = item.xpath('@href').extract()[0]
                    url = 'http://unity3d.com/%s' % url
                    title = item.xpath('text()').extract()[0]
                    video = {
                        'number': number,
                        'url': url,
                        'title': title.strip(),
                    }
                    cur_level['videos'].append(video)
                    yield Request(url, callback=self.parse_video,
                                  meta={'cur_path': cur_path,
                                        'cur_topic_idx': cur_topic_idx,
                                        'cur_level_idx': cur_level_idx,
                                        'cur_video_idx': number-1})
            else:
                print 'End Section.'


    def parse_video(self, response):
        sel = Selector(response)
        meta = response.request.meta
        self.log('The meta: %r' % meta)
        cur_path = meta['cur_path']
        cur_topic_idx = meta['cur_topic_idx']
        cur_level_idx = meta['cur_level_idx']
        cur_video_idx = meta['cur_video_idx']
        cur_video = self.topics[cur_topic_idx]['levels'][cur_level_idx]['videos'][cur_video_idx]
        self.log('Current video: %r' % cur_video)
        
        descr = sel.css('.g9.mb10 p').xpath('text()').extract()[0]
        if descr:
            cur_video['descr'] = descr.strip()
            self.log('Got descr > [%s]' % descr)
        else:
            self.log('Descr failed >>>>>>>> [%s]' % response.url)
        
        youtube_key = sel.css('.g9.lesson-video.ic iframe').xpath('@src').re('http://.*youtube.com/embed/([^?]*)\?')[0]
        if youtube_key:
            cur_video['youtube_key'] = youtube_key
            os.system('cd /tmp/videos && proxychains youtube-dl http://www.youtube.com/watch\?v\=%s --write-sub --all-subs --write-auto-sub' % youtube_key)
            os.system('mv /tmp/videos/*%s* %s' % (youtube_key, cur_path))
            self.log('Got youtube key > %s' % youtube_key)
        else:
            self.log('Youtube key failed >>>>>>>> [%s]' % response.url)


    def spider_closed(self, spider):
        pprint(self.topics)
        with open('videos/topics.json', 'w') as f:
            json.dump(self.topics, f)
