import json
from pathlib import Path
from typing import Any

class PublicDataLoader:
    """
    data/서울 폴더 안의 모든 JSON 파일을 안전하게 로드합니다.
    """
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        self.data: dict[str, Any] = {}

    def load_directory(self) -> dict[str, Any]:
        if not self.directory_path.exists():
            raise FileNotFoundError(f"디렉터리를 찾을 수 없습니다: {self.directory_path}")

        if not self.directory_path.is_dir():
            raise NotADirectoryError(f"디렉터리가 파일 경로입니다: {self.directory_path}")

        json_files = sorted(self.directory_path.glob("*.json"))
        if not json_files:
            raise FileNotFoundError(f"JSON 파일이 없습니다: {self.directory_path}")

        for json_path in json_files:
            self.data[json_path.stem] = self._load_file(json_path)

        return self.data

    def _load_file(self, json_path: Path) -> Any:
        try:
            with json_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON 파싱 오류: {json_path} - {exc.msg}") from exc
        except PermissionError as exc:
            raise PermissionError(f"파일 접근 권한이 없습니다: {json_path}") from exc