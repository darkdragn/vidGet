import re
from bs4 import BeautifulSoup
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags = ['ah', 'animehaven']


class Series(vidSeries):
    siteTemplate = 'http://animehaven.org/{}'
    seriesTemplate = siteTemplate
    matchIt = re.compile('Episodes.*')

    def formatPage(self, in_val):
        return in_val

    def pageList(self):
        list_args = {'name': 'select', 'id': 'episodes_list_selectbox'}
        try:
            initial_url = self.soup.find('a', text=self.matchIt)['href']
            base = 'http://animehaven.to/dubbed/'
        except:
            temp = self.seriesTemplate.format('episodes/subbed')
            initial_url = self.listPages('/'.join([temp, self.name]))
            base = 'http://animehaven.to/subbed/'
        initial = webpage(initial_url)
        first = webpage(initial.soup.findAll('h2')[0].a['href'])
        epi_data = [i['data-slug']
                    for i in first.soup.find(**list_args)('option')[::-1]]
        return [''.join([base, i]) for i in epi_data]

    def runExtras(self):
        for i in self.extras:
            if 'dub' in i:
                self.matchIt = re.compile('English.*Dub.*')
            elif 'pref' in i:
                self.pref = i.split('=')[-1]

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
