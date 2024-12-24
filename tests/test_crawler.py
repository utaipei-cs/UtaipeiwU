import aiofiles
import pytest

from course_crawler.crawler import Crawler
from course_crawler.model import Course


@pytest.mark.anyio
async def test_parse_html():
    crawler = Crawler()
    async with aiofiles.open(
        "tests/data/ag304_03.html", mode="r", encoding="utf-8"
    ) as f:
        content = await f.read()
        df = crawler.parse_html(content)
        assert df.loc[0, "科目"] == "服務學習"
        assert df.loc[1, "科目"] == "脊椎動物學"
        assert df.shape == (17, 12)


def test_parse_course_info():
    crawler = Crawler()
    course_data1 = {
        "選課代碼": "0833",
        "科目": "服務學習",
        "分組": "01",
        "學分": "0",
        "時數": "0",
        "必選修": "【必修】",
        "開課別": "【學期】",
        "校區": "博愛",
        "上課教師/時間/教室": "李孟陽時間未定(教室未定)",
        "領域類": "服務學習類",
        "限制性別": "不限",
        "教學綱要": "教學綱要",
    }
    course1 = crawler.parse_course_info(course_data1)
    assert (
        course1.model_dump()
        == Course(
            id="0833",
            name="服務學習",
            credit="0",
            field="服務學習類",
            area="博愛",
            time="時間未定",
            room="教室未定",
            teacher="李孟陽",
            english=False,
            type=1,
        ).model_dump()
    )

    course_data2 = {
        "選課代碼": "2524",
        "科目": "桌球",
        "分組": "14",
        "學分": "0",
        "時數": "2.0",
        "必選修": "【必修】",
        "開課別": "【學期】",
        "校區": "博愛",
        "上課教師/時間/教室": "韓大衛 (一)8-9(B106桌球教室)",
        "領域類": "體育類",
        "限制性別": "不限",
        "教學綱要": "教學綱要",
    }
    course2 = crawler.parse_course_info(course_data2)
    assert (
        course2.model_dump()
        == Course(
            id="2524",
            name="桌球",
            credit="0",
            field="體育類",
            area="博愛",
            time="M8M9",
            room="B106桌球教室",
            teacher="韓大衛",
            english=False,
            type=1,
        ).model_dump()
    )
