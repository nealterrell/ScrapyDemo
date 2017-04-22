import scrapy
from bs4 import BeautifulSoup

# The content of the blog posts has ugly HTML in it. Let's strip it out.

# BeautifulSoup4 is a library for removing HTML tags, leaving only the content within.
# We can also fully remove the content of certain tags, like <script> and <style>.
def strip_html(text):
    # Constructs a parser/stripper for the given text.
    soup = BeautifulSoup(text, 'html.parser')
    # Remove <script> and <style> tags, INCLUDING their immediate content, which is
    # probably meaningless to us.
    for badTag in ['script', 'style']:
        to_extract = soup.findAll(badTag)
        for item in to_extract:
            item.extract()

    # With the bad tags completely gone, get_text() will replace all other tags
    # with only their content.
    return soup.get_text().replace('\n', ' ').strip()

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for article in response.css('article'):
            title = article.css('h2.entry-title')
            content = article.css('div.entry-summary')
            yield {'title': title.css('a ::text').extract_first(),
                   # Use our strip_html function to remove HTML tags from the content.
                   'content': strip_html(content.css('p').extract_first())}

        next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)