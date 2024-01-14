import requests as rq
from bs4 import BeautifulSoup
import sys
from threading import Thread
from queue import Queue
import time

LINKS = ["https://www.nytimes.com/section/world/europe", 
         "https://www.nbcnews.com/", 
         'https://www.aljazeera.com/news/']

DATA = []
STOP = False
SLEEP = 120


class NewsAggregator:
    def __init__(self, url, queue, index):
        self.url = url
        self.queue = queue
        self.index = index
        
    def getData(self):
        res = rq.get(self.url)
        return res.text
    
    def parseNewsFirst(self):
        htmlData = self.getData()
        parser = BeautifulSoup(htmlData, "html.parser")
        
        newsData = []
        
        title = parser.head.find('title')
        
        section = parser.find('section', id = 'stream-panel')
        newsList = section.find_all('li', class_= 'css-18yolpw')

        
        for news in newsList:
            text = news.find('p', class_='css-1pga48a e15t083i1')
            author = news.find('span', class_ = 'css-1n7hynb')
            
            # Со временем проблемы, т.к. там стоит селектор ::after, не могу понять как его учесть, иначе выдает None
            # time = news.find('div', class_='css-e0xall e15t083i3')
            
            if text is None or author is None:
                continue
            
            item = {
                'title': title.text,
                'time' : "No time",
                'text' : text.text,
                "author": author.text 
            }
            self.queue.put(item) 
            
            
        
        return 0
        
    def parseNewsSecond(self):
        htmlData = self.getData()
        parser = BeautifulSoup(htmlData, "html.parser")
        
        newsData = []
        
        title = parser.head.find('title')
        section = parser.find('div', class_='rail__wrapper')
        newsList = section.findAll('li', class_='styles_item__1iZnY')
        for news in newsList:
            text = news.find('a')
            time = news.find('div', class_ = 'styles_teaseTimestamp__B7QIY')
            
            if text is None or time is None:
                continue
            
            item = {
                'title': title.text,
                'time' : time.text,
                'text' : text.text,
                "author": "no author" 
            }
            self.queue.put(item) 
            
            
        
        return 0
        
        
         
    def parseNewsThird(self):
        htmlData = self.getData()
        parser = BeautifulSoup(htmlData, "html.parser")
        
        title = parser.head.find('title')
        section = parser.find('section', id="news-feed-container")
        newsList = section.find_all('article', class_='gc u-clickable-card gc--type-post gc--list gc--with-image')
        for news in newsList:
            text = news.find('div', class_='gc__excerpt').find('p')
            time = news.find('div', class_='date-simple css-1yjq2zp').find('span', attrs={'aria-hidden':'true'})
            
            if text is None or time is None:
                continue
                        
            item = {
                'title': title.text,
                'time' : time.text,
                'text' : text.text,
                "author": "no author" 
            }
            self.queue.put(item) 
                       
            
        
        return 0
    
    def parsing(self):
        while True:
            if self.index == 0:
                self.parseNewsFirst()
                # self.queue.put(data)
            if self.index == 1:
                self.parseNewsSecond()
                # self.queue.put(data)
            if self.index == 2:
                self.parseNewsThird()
                # self.queue.put(data)
                
            time.sleep(SLEEP)
            
    
    
class Cycle:
    def __init__(self):
        self.queue = Queue()
        self.newsFirst = NewsAggregator(LINKS[0], self.queue, 0);
        self.newsSecond = NewsAggregator(LINKS[1], self.queue, 1);
        self.newsThird = NewsAggregator(LINKS[2], self.queue, 2);
        
    def start(self):
        t1 = Thread(target=self.newsFirst.parsing)
        t1.start()
        t2 = Thread(target=self.newsSecond.parsing)
        t2.start()
        t3 = Thread(target=self.newsThird.parsing)
        t3.start()
        
        while True:
            try:
                notEmpty = self.queue.not_empty
                if notEmpty:
                    item = self.queue.get()
                    helper = True
                    for el in DATA:
                        if el == item:
                            helper = False
                    if helper:
                        DATA.append(item)
                        print(f"Website: {item['title']}")
                        print(f"News time: {item['time']}")
                        print(f"News text: {item['text']}")
                        print(f"News author: {item['author']}")
                        print("\n\n\n")
                        
                    time.sleep(1) #Можно закомментить для дебага 
                        
            except KeyboardInterrupt:
                print('The program has stopped')
                exit(1)                
                
                
                        
                        
                
            


        
if __name__ == '__main__':
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    
    mainThread = Cycle()
    mainThread.start()
    
    