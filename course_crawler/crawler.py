import json
import re
from io import StringIO
from pathlib import Path
from typing import Generator

import aiofiles
import httpx
import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from yarl import URL

from course_crawler.model import Course
from course_crawler.utils.constant import (
    COURSE_TYPE,
    DEPARTMENT,
    FIELD_VALUE_NOT_SET,
    GRADE,
    HOST,
    SECTION_TO_ENG,
    WEELDAT_IN_ENG,
)


class Crawler:
    def __init__(self):
        self.year = "113"
        self.semester = "2"
        self.courses = {}

    async def run(self) -> None:
        transport = httpx.AsyncHTTPTransport(retries=3, verify=False)
        async with httpx.AsyncClient(transport=transport, verify=False) as client:
            await self.run_with_client(client)

        filename = f"{self.year}{self.semester}0-data.json"
        full_path = Path("parse-data") / filename
        async with aiofiles.open(full_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self.courses, ensure_ascii=False, indent=2))

        full_path = Path("public/course-data") / filename
        async with aiofiles.open(full_path, "w", encoding="utf-8") as f:
            await f.write(json.dumps(self.courses, ensure_ascii=False))

    async def run_with_client(self, client: httpx.AsyncClient) -> None:
        for prefix, url in self.generate_urls():
            logger.info(f"Fetching {url}")
            response = await client.get(url)
            response.raise_for_status()
            df = self.parse_html(response.text)
            self.parse_courses(prefix, df)

    def generate_urls(self) -> Generator[tuple[str, str], None, None]:
        link = URL.build(
            scheme="https",
            host=HOST,
            path="/utaipei/ag_pro/ag304_03.jsp",
            query={
                "arg01": self.year,
                "arg02": self.semester,
                "arg": "XS001400",
                "uid": "null",
            },
        )
        prefix = self.year + self.semester + "0" + "XS00" + "1"
        yield prefix, str(link)

        for i in range(0, len(DEPARTMENT)):
            for j in range(1, 9):
                link = URL.build(
                    scheme="https",
                    host=HOST,
                    path="/utaipei/ag_pro/ag304_03.jsp",
                    query={
                        "arg01": self.year,
                        "arg02": self.semester,
                        "arg": DEPARTMENT[i] + GRADE[j],
                        "uid": "null",
                    },
                )
                prefix = self.year + self.semester + "0" + DEPARTMENT[i] + str(j)
                yield prefix, str(link)
            # break

    def parse_html(self, raw_data: str) -> pd.DataFrame:
        soup = BeautifulSoup(raw_data, "html.parser")
        table = soup.find("table")

        try:
            df = pd.read_html(StringIO(str(table)))[0]
        except ValueError:
            return pd.DataFrame()

        df.columns = pd.Index(df.iloc[0].tolist())  # 將第 0 列設為欄位名稱
        df = df[1:]  # 刪除第 0 列
        df.reset_index(drop=True, inplace=True)  # 重設索引
        return df

    def parse_courses(self, prefix: str, df: pd.DataFrame) -> None:
        course_datas = df.to_dict(orient="records")
        for coruse_data in course_datas:
            course = self.parse_course_info(prefix, coruse_data)
            self.courses[course.id] = course.model_dump()

    def parse_course_info(self, prefix: str, course_data: dict) -> Course:
        pattern1 = re.compile(
            r"(?P<teacher>.*\s)(?P<day>[(（][一二三四五六日][)）])(?P<start>\d+)-(?P<end>\d+)(?P<room>[(（].*[)）])"
        )
        match1 = pattern1.match(str(course_data["上課教師/時間/教室"]))
        pattern2 = re.compile(
            r"(?P<teacher>.*)(?P<day>時間未定)(?P<room>[(（]教室未定[)）])"
        )
        match2 = pattern2.match(str(course_data["上課教師/時間/教室"]))

        teacher = FIELD_VALUE_NOT_SET
        room = FIELD_VALUE_NOT_SET
        time = ""
        if match1 is not None:
            week = (
                match1.group("day").strip("()（）")
                if match1.group("day")
                else FIELD_VALUE_NOT_SET
            )
            start_time = match1.group("start") if match1.group("start") else 0
            end_time = match1.group("end") if match1.group("end") else 0
            for section in range(int(start_time), int(end_time) + 1):
                if section > 9:
                    time += f"{WEELDAT_IN_ENG[week]}{SECTION_TO_ENG[section]}"
                else:
                    time += f"{WEELDAT_IN_ENG[week]}{section}"

            room = (
                match1.group("room").strip("()（）")
                if match1.group("room")
                else FIELD_VALUE_NOT_SET
            )

            teacher = match1.group("teacher").strip()
            teacher = teacher.replace(f"({week}){start_time}-{end_time}({room})", "、")
            teacher = teacher.replace(" ", "")

        elif match2 is not None:
            teacher = match2.group("teacher").strip()
            time = match2.group("day")
            room = match2.group("room").strip("()（）")

        course = Course(
            id=prefix + course_data["選課代碼"],
            name=course_data["科目"],
            credit=course_data["學分"],
            field=course_data["領域類"],
            area=course_data["校區"],
            time=time,
            room=room,
            teacher=teacher,
            english=False,
            type=COURSE_TYPE[course_data["必選修"]],
        )
        return course
