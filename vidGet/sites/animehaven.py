import re
import requests

from multiprocessing import Pool
from bs4 import BeautifulSoup
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags = ['ah', 'animehaven']


def getSet(inVars):
    i_url, page = inVars
    url = '/'.join([i_url, 'page', str(page)])
    soup = bs4(requests.get(url).content, 'html.parser')
    return [i.a['href'] for i in soup.findAll('h2')]


class Series(vidSeries):
    siteTemplate = 'http://animehaven.org/{}'
    seriesTemplate = siteTemplate
    matchIt = re.compile('Episodes.*')

    def runExtras(self):
        for i in self.extras:
            if 'dub' in i:
                self.matchIt = re.compile('English.*Dub.*')
            elif 'pref' in i:
                self.pref = i.split('=')[-1]

    def listPages(self, url):
        initial = webpage(url)
        try:
            pagination = initial.soup.find('nav', class_='pagination')
            lp = int(pagination.findAll('a')[-1]['href'].split('/')[-1])
        except AttributeError:
            lp = 1
        pool = Pool(processes=4)
        pages = pool.map(getSet, [(url, x) for x in range(1, lp+1)])
        pool.close()
        return [self.page(p, self) for i in pages[::-1] for p in i[::-1]]

    @property
    @memorize
    def pages(self):
        try:
            initial_url = self.soup.find('a', text=self.matchIt)['href']
            return self.listPages(initial_url)
        except:
            temp = self.seriesTemplate.format('episodes/subbed')
            return self.listPages('/'.join([temp, self.name]))

    class page(vidSeries.page):

        @property
        @memorize
        def embedLink(self):
            count = 0
            while True:
                try:
                    if count > 2:
                        break
                    return self.soup.find(
                            'div',
                            class_='download_feed_link').a['href']
                except AttributeError:
                    self.soup = bs4(self.source)
                    count += 1

        @property
        @memorize
        def video(self):
            pref, self.strainOnly = ['720', '480'], 'a'
            if hasattr(self.series, 'pref'):
                next(pref.insert(0, pref.pop(pref.index(i)))
                     for i in pref if self.series.pref in i)
            try:
                return next(dlink['href'] for qual in pref
                            for dlink in self.soup.findAll('a', class_='btn')
                            if qual in dlink.text)
            except:

                urlTemp = 'http://{}/{}/v.mp4'
                embed = webpage()
                if not self.embedLink:
                    return
                embed.url = self.embedLink
                group_full = embed.soup.find('div', class_='left')
                group = group_full.parent.script.text.split('|')
                firstHit = re.search("img src=\"http://([^/]*)/",
                                     embed.source).group(1)
                pot = next(num for qual in pref
                           for num, i in enumerate(group)
                           if qual == i)
                if 'label' in group[pot+1]:
                    pot = pot+2
                return urlTemp.format(firstHit, group[pot+1])
