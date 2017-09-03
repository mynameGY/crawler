# -*- coding: utf-8 -*-
import scrapy

from crawler.items import MyItem

class NgaSpders(scrapy.Spider):
    name = "NgaSpider"
    currName = ""
    #host = "http://bbs.ngacn.cc/"
    # start_urlsÊÇÎÒÃÇ×¼±¸ÅÀµÄ³õÊ¼Ò³
    def start_requests(self):
        urls = [
           # 'https://www.zhihu.com/question/60543259/answer/177762193',
            'http://wordcookies.info/pumpkin/level-7.html'
        ]
        for url in urls:
            yield scrapy.Request(url = url,callback=self.getData)

	# Õâ¸öÊÇ½âÎöº¯Êý£¬Èç¹û²»ÌØ±ðÖ¸Ã÷µÄ»°£¬scrapy×¥»ØÀ´µÄÒ³Ãæ»áÓÉÕâ¸öº¯Êý½øÐÐ½âÎö¡£
    # ¶ÔÒ³ÃæµÄ´¦ÀíºÍ·ÖÎö¹¤×÷¶¼ÔÚ´Ë½øÐÐ£¬Õâ¸öÊ¾ÀýÀïÎÒÃÇÖ»ÊÇ¼òµ¥µØ°ÑÒ³ÃæÄÚÈÝ´òÓ¡³öÀ´¡£
    def parse(self, response):
        print '+++++++++++++++++++'
        for quote in response.xpath('//ul/li'):
            link =  quote.xpath('a/@href').extract()
            if len(link) >0: 
                print link
                currName = quote.xpath('a/text()').extract()
                print currName
                url = 'http://wordcookies.info%s'%(link[0])    
                print url    

                yield scrapy.Request(url = url,callback=self.getLevelLink)

                return;    
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            } 

        return;        
        page = response.url.split("/")[-2]
        print "page:  ----   "+page
        filename = 'quotes-%s.html'%page
        with open(filename,'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


    def getLevelLink(self, response):  
        for quote in response.xpath('//ul/li'):
            link = quote.xpath('a/@href').extract()
            if len(link) >0:
                url = 'http://wordcookies.info%s'%(link[0]) 
                yield scrapy.Request(url = url,callback=self.getLevelLink)
                


    def getData(self, response):
        items = []
        for quote in response.xpath('//div[@class="words"]'):
            print "++++++++++++++"
            htmlStr = quote.extract()
            strLen = len(htmlStr)
            htmlStr =  htmlStr[20:strLen-6]   
            print htmlStr

            spans = htmlStr.split('<br>')
            print spans

            words = []
            for span in spans:
                span = span.strip()
                chars = "".join(span.split('<span>')).split('</span>')
                print chars
                if len("".join(chars)) > 0:
                    words.append("".join(chars))

            item = MyItem()
            item['chars'] = words
            items.append(item)
        return items 

            
                           