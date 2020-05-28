import sys
import os

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy", "crawl", "zhihu"])
# execute(["scrapy", "crawl", "lagou"])
# execute(["scrapy", "crawl", "zhilian"])
# execute(["scrapy", "crawl", "liepin"])
execute(["scrapy", "crawl", "boss"])

