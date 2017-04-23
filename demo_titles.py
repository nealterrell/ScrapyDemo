import scrapy


# This demo is courtesy of www.scrapy.org

# A Spider is responsible for registering URLs to download, and mapping
# documents that are downloaded to some data format.
class BlogSpider(scrapy.Spider):
    # These two fields tell Scrapy some basic info about our spider.
    name = "blogspider_titles"
    # start_urls contains a list of URLs that will kick off the scraping.
    # Other urls can be discovered and registered as the start_urls are processed.
    start_urls = ["https://blog.scrapinghub.com"]

    # parse is called with an HTML response to a URL that was either in start_urls,
    # or later registered with scrapy.Request.
    # parse should do at least one of the following for a response:
    # 1. Decide it should be ignored, based on the content of the document.
    # 2. Decide it should be saved as a document in the final output, by using yield
    #    to return a dictionary of content you wish you save for the document.
    # 3. Register new URLs to download based on the content of the document.
    def parse(self, response):
        # response contains a DOM-like state that can be navigated with
        # CSS selectors or with XPath expressions.

        # response.css takes a CSS selector, in this case returning any h2 element
        # of the css class "entry-title".
        for title in response.css("h2.entry-title"):
            # "a ::text" selects an anchor tag"s (<a>) inner text attribute.
            # extract() and extract_first() return the string contained by the
            # given HTML element; otherwise we get a complex object.
            yield {"title": title.css("a ::text").extract_first()}

        # Now that we have parsed all the blog entries on this page, we see if there
        # is a new URL for the spider to crawl.

        # The > selector returns all the *immediate children* of the previously-
        # identified element. In this case, we return all the <a> children of a div
        # with the "prev-post" class. ::attr(href) returns the href="..." attribute
        # of the anchor.
        next_page = response.css("div.prev-post > a ::attr(href)").extract_first()
        if next_page:
            # Tell Scrapy to crawl this new URL, adding it to the crawl queue.
            # The method parse (the one we are in) will be called with the results.
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
