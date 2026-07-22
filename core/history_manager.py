import json
from pathlib import Path

from core.history import HistoryRecord


class HistoryManager:
    """占卜紀錄管理"""

    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)

        self.file_path = self.data_dir / "history.json"

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
        print("save()")
        print(self.file_path)
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

    def get(self, record_id: str):
        """取得單筆紀錄"""

        for item in self.records:
            if item.id == record_id:
                return item

        return None

    def get_all(self):
        """取得所有紀錄"""

        return self.records.copy()

    def clear(self):
        """清空所有紀錄"""

        self.records.clear()
        self.save()