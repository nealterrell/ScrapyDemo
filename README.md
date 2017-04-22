# Scrapy Demo
A demonstration of web scraping with Scrapy at [BeachHacks 2017](http://beachhacks.com)

## Slides

https://docs.google.com/presentation/d/1cSV-Am9tGczHIwJcEjyTKUtRmmkv3MIGBFCR89pFZ_Q/edit?usp=sharing

## Running the demos

Requires Python 3+. I like [Anaconda](https://www.continuum.io/downloads).

1. Install [Scrapy](https://scrapy.org). In Anaconda: `conda install -c conda-forge scrapy=1.3.3`
2. Install BeautifulSoup4: `conda install -c anaconda beautifulsoup4=4.5.3`
3. Run a demo from a command line:
    1. `scrapy runspider demo_titles.py -o output_titles.json` -- scrapes the titles of blog posts from https://blog.scrapinghub.com/
    2. `scrapy runspider demo_content.py -o output_content.json` -- scrapes titles and (unstripped) content from the same URL
    3. `scrapy runspider demo_content_beautiful.py -o output_beautiful.json` -- scrapes titles and stripped content via BeautifulSoup.

