import scrapy

# In demo_titles, our output only had the title of each blog post. What if we wanted
# the content too?


class BlogSpider(scrapy.Spider):
    name = "blogspider_content"
    start_urls = ["https://blog.scrapinghub.com"]

    def parse(self, response):
        # We don"t want to iterate only over the titles anymore; we want to iterate
        # over the <article> entries.
        for article in response.css("article"):
            # Ask this article for its title
            title = article.css("h2.entry-title")
            # Ask this article for its content summary div.
            content = article.css("div.entry-summary")
            yield {"title": title.css("a ::text").extract_first(),
                   # The content div"s first <p> has the actual content.
                   "content": content.css("p").extract_first()}

        next_page = response.css("div.prev-post > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)