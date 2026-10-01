from pathlib import Path


def file_reader(file_path: str) -> str:

    try:

        path = Path(file_path)

        if not path.exists():
            return f"File not found: {file_path}"

        if not path.is_file():
            return f"Not a file: {file_path}"

        content = path.read_text(
            encoding="utf-8"
        )

        return content

    except Exception as e:

        return f"File reading error: {str(e)}"