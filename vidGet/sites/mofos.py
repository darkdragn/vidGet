import re
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, webpage, initMech
except ImportError:
    from vidsite import vidSeries
    from util import memorize, webpage, initMech

class mofos(vidSeries):
    pageCheck      = True
    siteTemplate   = 'http://members2.mofos.com{}'
    seriesTemplate = siteTemplate.format('/model/{}')
    tags, type_    = ['m', 'mofos'], 'Model'
    
    def __init__(self, series, extras=None, cookie=None):
        if extras:
            self.extras = extras.split(',')
            self.runExtras()
        self.name = series
        self.br = initMech(self.siteTemplate.format(''))
        self.auth()
    
    def auth(self):
        if not hasattr(self, 'username') or not hasattr(self, 'password'):
            raise ValueError("Please pass user and pass extra options.")
        self.br.select_form(nr=0)
        self.br['username'], self.br['password'] = self.username, self.password
        try:
            self.br.submit()
        except:
            pass
        self.br.select_form(nr=0)
        self.br.submit()
        
    @property
    def title(self):
        return self.soup.find('div', 
                              class_='model-name').text.replace(u'\xa0', '_')
    @property
    def pages(self):
        return [self.page(self.siteTemplate.format(i['href']), self) 
                for i in self.soup.find('section', class_='girl-videos').findAll('a') 
                if 'scene/view' in i['href'] ]
                
    def runExtras(self):
        for i in self.extras:
            if 'user' in i:
                self.username = i.split('=')[-1]
            if 'pass' in i:
                self.password = i.split('=')[-1]
        
    class page(vidSeries.page):
        @property
        @memorize
        def name(self):
            return self.videoUrl.info().get('content-disposition').split('=')[-1]
        @property
        @memorize
        def video(self):
            return self.videoUrl.geturl()
        @property
        @memorize
        def videoUrl(self):
            pref = ['720p', 'MPEG4']
            url = next(self.series.siteTemplate.format(o['href']) for i in pref 
                       for o in self.soup.find('div', class_='download-frame').findAll('a') 
                       if i in o.text)
            return self.series.br.open(url)
