import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from ..vidsite import vidSeries
from ..util import memorize, webpage

bs4 = BeautifulSoup
tags  = ['ha', 'hanime']

class Series(vidSeries):
    siteTemplate   = 'https://hanime.tv{}'
    seriesTemplate = siteTemplate.format('/hentai-videos/{}-1')
    single = False

    @property
    def pages(self):
        f = lambda x: x.split('?r=')
        li = [a['href'] for a in self.soup(class_='franchise-list')[0]('a')]
        out = [self.page(self.url)]
        out.extend([self.page(self.siteTemplate.format(i)) for i in li
            if not f(i)[0] == f(i)[1]])
        return out
        # for i in li:
            # yield self.page(self.siteTemplate.format(i))

    @property
    @memorize
    def title(self):
        if self.single:
            span = self.soup.h1
        else:
            try:
                span = self.soup('div', class_='section-title')[0]('span')[1]
            except:
                self.single = True
                return self.title
        return span.text.replace(' ', '_')

    def runExtras(self):
        self.seriesTemplate = self.siteTemplate.format('/hentai-videos/{}')
        self.pages = [self.page(self.url)]
        self.single = True


    class page(vidSeries.page):
        def run_multi(self, m3_url, fn):
            mani = 'https://hanime.tv/api/v2/hentai_video_manifests/{}'
            m3u8 = requests.get('https://hanime.tv{}'.format(m3_url)).content
            p_url = next(i for i in m3u8.split('\n') if 'm3u8' in i)
            p_url = mani.format(p_url)
            m3_full = requests.get(p_url)
            m3_list = m3_full.content.split('\n')
            p_list = [h for h in m3_list if h.startswith('http')]
            with open(fn, 'wb') as f:
                for part in tqdm(p_list):
                    temp = requests.get(part, stream=True)
                    for buf in temp.iter_content(1024):
                        f.write(buf)
                    f.flush()

        @property
        def video(self):
            pref = ('720', '480')
            # comp = re.compile('height":"(.*?)","url":"(.*?)"')
            comp = re.compile('height":(.*?),"url":"(.*?)"')
            li = comp.findall(self.source)
            ret = next(a[1] for i in pref for a in li if i in a[0])
            if 'm3u8' in ret:
                return self.run_multi, ret
            return ret
