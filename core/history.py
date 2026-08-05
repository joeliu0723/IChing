from dataclasses import dataclass, field
from datetime import datetime
from typing import List


VERIFICATION_RESULTS = (
    "未驗證",
    "符合",
    "部分符合",
    "不符合",
)


@dataclass
class HistoryRecord:
    """單筆占卜紀錄"""

    id: str = ""

    created_at: datetime = field(default_factory=datetime.now)

    # 占問問題
    question: str = ""

    # 六爻（由下往上）
    lines: List[str] = field(default_factory=list)

    # 本卦
    main_number: int = 0
    main_name: str = ""

    # 變卦
    changed_number: int = 0
    changed_name: str = ""

    # 動爻
    moving_lines: List[int] = field(default_factory=list)

    # 使用者心得
    notes: str = ""

    # 收藏
    favorite: bool = False

    # 事後驗證
    verification_content: str = ""
    verification_result: str = "未驗證"

    # 最後更新時間
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """轉成可儲存 JSON 的格式"""

        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "question": self.question,
            "lines": self.lines,
            "main_number": self.main_number,
            "main_name": self.main_name,
            "changed_number": self.changed_number,
            "changed_name": self.changed_name,
            "moving_lines": self.moving_lines,
            "notes": self.notes,
            "favorite": self.favorite,
            "verification_content": self.verification_content,
            "verification_result": self.verification_result,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """由 JSON 建立物件"""

        record = cls()

        record.id = data.get("id", "")
        created = data.get("created_at", datetime.now().isoformat())
        record.created_at = datetime.fromisoformat(created)

        updated = data.get("updated_at", created)
        record.updated_at = datetime.fromisoformat(updated)

        record.question = data.get("question", "")
        record.lines = data.get("lines", [])

        record.main_number = data.get("main_number", 0)
        record.main_name = data.get("main_name", "")

        record.changed_number = data.get("changed_number", 0)
        record.changed_name = data.get("changed_name", "")

        record.moving_lines = data.get("moving_lines", [])

        record.notes = data.get("notes", "")
        record.favorite = bool(data.get("favorite", False))

        record.verification_content = data.get(
            "verification_content",
            "",
        )

        result = data.get("verification_result", "未驗證")
        if result not in VERIFICATION_RESULTS:
            result = "未驗證"
        record.verification_result = result

        return record
