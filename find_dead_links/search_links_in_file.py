import re
from pathlib import Path

import pandas as pd

MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")


def search_links_in_markdown_files(directory: Path) -> pd.DataFrame:
    """Search for links in all markdown files within the given directory.

    Args:
        directory (Path): The directory to search for markdown files.

    Returns
    -------
        pd.DataFrame: A DataFrame containing found links with their file paths.
            Columns: ['file_path', 'text', 'url']
    """
    dataframes: list[pd.DataFrame] = []
    for file_path in directory.rglob("*.md"):
        with Path.open(file_path) as file:
            content = file.read()
            df_file_links = _search_links_in_markdown_text(content)
            if not df_file_links.empty:
                df_file_links["file_path"] = str(file_path).replace(str(directory) + "/", "")
                dataframes.append(df_file_links)
    res_columns = ["file_path", "text", "url"]
    if len(dataframes) == 0:
        return pd.DataFrame(columns=res_columns)
    return pd.concat(dataframes, ignore_index=True)[res_columns]


def _search_links_in_markdown_text(text: str) -> pd.DataFrame:
    # Regex to find markdown links: [text](url)
    matches = re.findall(MARKDOWN_LINK_PATTERN, text)
    data = [{"text": m[0], "url": m[1]} for m in matches]
    return pd.DataFrame(data)
