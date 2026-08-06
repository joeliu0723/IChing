import json
from pathlib import Path

from core.history import HistoryRecord, VERIFICATION_RESULTS
from core.paths import history_path, user_data_dir


SORT_BY_DATE = "date"
SORT_BY_MAIN = "main"
SORT_BY_FAVORITE = "favorite"
SORT_BY_VERIFICATION = "verification"

SORT_OPTIONS = (
    (SORT_BY_DATE, "日期"),
    (SORT_BY_MAIN, "本卦"),
    (SORT_BY_FAVORITE, "收藏"),
    (SORT_BY_VERIFICATION, "驗證結果"),
)

_VERIFICATION_ORDER = {
    name: index
    for index, name in enumerate(VERIFICATION_RESULTS)
}


class HistoryManager:
    """占卜紀錄管理"""

    def __init__(self):
        self.data_dir = user_data_dir()
        self.data_dir.mkdir(exist_ok=True)

        self.file_path = history_path()

        self.records = []

        self.load()

    def load(self):
        """讀取所有紀錄"""

        if not self.file_path.exists():
            self.records = []
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.records = [
                HistoryRecord.from_dict(item)
                for item in data
            ]

        except Exception:
            self.records = []

    def save(self):
        data = [
            record.to_dict()
            for record in self.records
        ]

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    def add(self, record: HistoryRecord):
        """新增紀錄"""

        self.records.insert(0, record)
        self.save()

    def update(self, record: HistoryRecord):
        """更新紀錄"""

        for index, item in enumerate(self.records):
            if item.id == record.id:
                self.records[index] = record
                self.save()
                return

    def delete(self, record_id: str):
        """刪除紀錄"""

        self.records = [
            item
            for item in self.records
            if item.id != record_id
        ]

        self.save()

    def delete_many(self, record_ids):
        """一次刪除多筆，只寫入檔案一次。"""

        id_set = set(record_ids)

        if not id_set:
            return

        self.records = [
            item
            for item in self.records
            if item.id not in id_set
        ]

        self.save()

    def get(self, record_id: str):
        """取得單筆紀錄"""

        for item in self.records:
            if item.id == record_id:
                return item

        return None

    def get_all(self):
        """取得所有紀錄"""

        return self.records.copy()

    def search(self, keyword: str):
        """
        搜尋紀錄。

        可搜尋：問題、卦名、卦序、收藏、驗證結果、驗證內容
        """

        text = (keyword or "").strip().lower()

        if not text:
            return self.get_all()

        if text in ("收藏", "★", "favorite"):
            return [
                record
                for record in self.records
                if record.favorite
            ]

        if text in {item.lower() for item in VERIFICATION_RESULTS}:
            return [
                record
                for record in self.records
                if record.verification_result.lower() == text
            ]

        results = []

        for record in self.records:
            if self._matches(record, text):
                results.append(record)

        return results

    def sort_records(
        self,
        records,
        sort_by: str = SORT_BY_DATE,
        ascending: bool = False,
    ):
        """
        排序紀錄。

        支援：日期、本卦、收藏、驗證結果。
        ascending=True：小→大／舊→新；False：大→小／新→舊。
        """

        items = list(records)
        key = (sort_by or SORT_BY_DATE).strip().lower()

        if key == SORT_BY_MAIN:
            items.sort(
                key=lambda record: (
                    record.main_number,
                    record.created_at,
                ),
                reverse=not ascending,
            )
            return items

        if key == SORT_BY_FAVORITE:
            # ascending：未收藏在前；descending：收藏在前
            items.sort(
                key=lambda record: (
                    record.favorite if ascending else not record.favorite,
                    -record.created_at.timestamp(),
                )
            )
            return items

        if key == SORT_BY_VERIFICATION:
            items.sort(
                key=lambda record: (
                    _VERIFICATION_ORDER.get(
                        record.verification_result,
                        0,
                    ),
                    -record.created_at.timestamp(),
                ),
                reverse=not ascending,
            )
            return items

        # 日期：ascending=舊→新；預設 descending=新→舊
        items.sort(
            key=lambda record: record.created_at,
            reverse=not ascending,
        )
        return items

    def _matches(self, record: HistoryRecord, keyword: str) -> bool:
        fields = [
            record.question,
            record.main_name,
            record.changed_name,
            str(record.main_number) if record.main_number else "",
            str(record.changed_number) if record.changed_number else "",
            record.verification_content,
            record.verification_result,
        ]

        return any(
            keyword in field.lower()
            for field in fields
            if field
        )

    def clear(self):
        """清空所有紀錄"""

        self.records.clear()
        self.save()
