# -*- coding: utf-8 -*-
import scrapy

class NgaSpders(scrapy.Spider):
    name = "NgaSpider"
    currName = ""
    #host = "http://bbs.ngacn.cc/"
    # start_urls������׼�����ĳ�ʼҳ
    def start_requests(self):
        urls = [
           # 'https://www.zhihu.com/question/60543259/answer/177762193',
            'http://wordcookies.info/pumpkin/level-7.html'
        ]
        for url in urls:
            yield scrapy.Request(url = url,callback=self.getData)

	# ����ǽ���������������ر�ָ���Ļ���scrapyץ������ҳ���������������н�����
    # ��ҳ��Ĵ���ͷ����������ڴ˽��У����ʾ��������ֻ�Ǽ򵥵ذ�ҳ�����ݴ�ӡ������
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
        for quote in response.xpath('//div[@class="words"]'):
            print "++++++++++++++"
            print quote    
            chars = quote.xpath('//br')
            print chars
            
                           