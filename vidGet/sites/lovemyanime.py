import re
try:
    from vidGet.vidsite import vidSeries
    from vidGet.util import memorize, runRepl, unescape, webpage
except ImportError:
    from vidsite import vidSeries
    from util import memorize, runRepl, unescape, webpage

class lovemyanime(vidSeries):
    siteTemplate   = 'http://www.lovemyanime.net{}'
    seriesTemplate = siteTemplate.format('/anime/{}')
    tags  = ['lma', 'lovemyanime']
    
    @property
    @memorize
    def pages(self):
        return [self.page(i.a['href'], self) for i in self.soup.findAll('div', class_='episode_list') ][::-1]
    class page(vidSeries.page):
        vidComps = ['file\': \'(?P<vid>.*)\'', 'source src=\'(.*)\' type']
        @property
        @memorize
        def embed(self):
            kickBack = webpage(self.embedLink)
            return webpage(self.embedLink)
        @property
        @memorize
        def embedLink(self):
            try:
                pref = ['Arkvid', 'Mp4upload Video']
                holdOther = next(i.a['href'] for p in pref 
                                             for i in self.soup.findAll('h3') 
                                             if p in i.a.text
                                             if hasattr(i, 'img'))
                self.soup = webpage(holdOther).soup
            except StopIteration:
                pass
            return self.soup.find('div', class_='videoembed').iframe['src']
        @property
        def video(self):
            for i in self.vidComps:
                try:
                    vidHold = re.search(i, self.embed.source).group(1)
                    if 'http' in vidHold:
                        return vidHold
                    return ''.join(['http:', vidHold])
                except AttributeError:
                    pass
                
