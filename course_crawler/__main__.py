import asyncio

from course_crawler.crawler import Crawler
from course_crawler.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    print(settings)
    crawler = Crawler()
    asyncio.run(crawler.run())


if __name__ == "__main__":
    main()
