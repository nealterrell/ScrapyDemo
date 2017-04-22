import scrapy
from bs4 import BeautifulSoup

# Scrapes pages from the individual sites set up by the United States National Park Service
# regarding each of the physical locations it administers.

def strip(text):
    soup = BeautifulSoup(text, 'html.parser')
    for badTag in ['script', 'style']:
        to_extract = soup.findAll(badTag)
        for item in to_extract:
            item.extract()
    return soup.get_text().replace('\n', ' ').strip()

    
class NPSpider(scrapy.Spider):
    name = 'National Park Service articles'
    # The NPS has a nice sitemap organized per state. Our start_urls will contain the base index
    # pages for each of the states. (Plus VI, for the United States Virgin Islands.)

    # 51 state abbreviations.
    stateList = ["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU","HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME","MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]

    # Variables to select only a subrange of the full state list. Set these variables to
    # 0 and -1 respectively to select all states.
    start_state = 6
    num_states = 1

    start_urls = ['https://www.nps.gov/state/' + state + '/index.htm'\
                  for state in stateList[start_state:start_state+num_states]]

    # parse is called for each of the start_urls, which are the per-state index pages.
    def parse(self, response):
        # Can help with logging.
        self.logger.info("URL:" + response.url)
#
        # The index pages contain links to each of the park sites for the given state.
        for park in response.css("#list_parks > li.clearfix"):
            name = park.css("h3 a::text").extract_first()
            if name is None:
                name = ''

            url = park.css("h3 a::attr(href)").extract_first()
            
            title = park.css("h2::text").extract_first()
            if title is None:
                title = ''
            
            location = park.css("h4::text").extract_first()
            if location is None:
                location = ''

            # Each park has a siteindex with links to all i ts content pages.
            full_url = "https://www.nps.gov" + url + "siteindex.htm"
            request = scrapy.Request(full_url, callback=self.parse_mainpage)
            # We can pass information to the spider callback as "meta", allowing us to send
            # information that might not be available in the next response.
            request.meta['park'] = {"name": name, "url": url, "title": title, "location": location}
            yield request

    # Parses the siteindex page for a given park.
    def parse_mainpage(self, response):
        park = response.meta['park']
        for article in response.css("div#npsNav > ul li"):
            link = article.css("a")
            title = link.css("::text").extract_first()
            title = strip(title) if title is not None else strip(article.xpath("a/span/text()").extract_first())

            full_url = "https://www.nps.gov" + link.css("::attr(href)").extract_first()
            request = scrapy.Request(full_url, callback=self.parse_page)
            request.meta['park'] = park
            request.meta['page'] = {"title": park["name"] + \
                                    (" " + park["title"] if len(park["title"]) > 0 else "") + ": " + title}
            yield request


    # This parses an individual article. Note that this is the only place a dictionary is yielded,
    # instead of a scrapy Request.
    def parse_page(self, response):
        info = response.meta['page']

        #div.ColumnMain.col-sm-12

        article = response.css("#main > div.container > div > div:nth-of-type(3)")
        yield {
            "title": info["title"],
            "body": strip(article.extract_first()),
            "url": response.url
        }