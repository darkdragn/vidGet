import re
import urllib2

try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, runRepl, unescape, webpage
except ImportError:
    from vidsite import vidSeries
    from util import memorize, runRepl, unescape, webpage

class animehaven(vidSeries):
    siteTemplate = 'http://animehaven.org/{}'
    seriesTemplate = siteTemplate
    tags = ['ah', 'animehaven']
    matchIt = re.compile('Episodes.*')
    
    def runExtras(self):
        for i in self.extras.split(','):
            if 'dub' in i:
                self.matchIt = re.compile('Episodes.*Dub.*')
    def listPages(self, url, cp=1, lp=None):
        curUrl = url if cp == 1 else '/'.join([url, 'page', str(cp)])
        intUrlObj = webpage(curUrl, self.br)
        if not lp:
            try:
                lp = int(intUrlObj.soup.find('nav', class_='pagination').findAll('a')[-1]['href'].split('/')[-1])
            except AttributeError:
                lp = 1
        pages = [self.page(i.h2.a['href'], self) for i in intUrlObj.soup.findAll('article')]
        if cp < lp:
            pages.extend(self.listPages(url, cp+1, lp))
        return pages
    @property
    @memorize
    def pages(self):
        return self.listPages(self.soup.find('a', text=self.matchIt)['href'])[::-1]
        
    class page(vidSeries.page):
        
        @property
        @memorize
        def video(self):
            sites = {'streamcannon': '<source src="(?P<vid>[^"]*)"', 'mp4upload': '\'file\': \'(?P<vid>[^\']*)\'',
                     'docs.google': 'url_encoded_fmt_stream_map"[^"]*"[^h]*(?P<vid>[^\\\\]*)\\\\'}
            try:
                return next(dlink['href'] for qual in ['720', '480']
                            for dlink in self.soup.find('div', class_='download_feed_link').findAll('a')
                            if qual in dlink.text)
                
            except:
                try:
                    embedLinks = self.soup.find('div', id=re.compile('tabs.*'))
                except:
                    return None
                for i in embedLinks.findAll('iframe'):
                    try:
                        embed = webpage(i['src'])
                        for site, pattern in sites.iteritems():
                            if site in embed.url:
                                self.vidComp = re.compile(pattern)
                        return unescape(self.runRepl(self.vidComp.search(embed.source)))
                    except:
                        pass
