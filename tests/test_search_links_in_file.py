from pathlib import Path

from find_dead_links.search_links_in_file import search_links_in_markdown_files


class TestSearchLinksInMarkdownFiles:
    def test_when_no_files_then_empty_dataframe(
        self,
        tmp_path: Path,
    ):
        df_links = search_links_in_markdown_files(tmp_path)
        assert df_links.empty

    def test_when_no_markdown_files_then_empty_dataframe(
        self,
        tmp_path: Path,
    ):
        (tmp_path / "test.txt").write_text("This is a test file: https://example.com.")
        df_links = search_links_in_markdown_files(tmp_path)
        assert df_links.empty

    def test_when_file_with_no_links_then_empty_dataframe(
        self,
        tmp_path: Path,
    ):
        (tmp_path / "test.md").write_text("This is a markdown file with no links.")
        df_links = search_links_in_markdown_files(tmp_path)
        assert df_links.empty

    def test_when_one_file_with_links_then_dataframe_with_link(
        self,
        tmp_path: Path,
    ):
        (tmp_path / "test.md").write_text("[link text](https://example.com)")
        df_links = search_links_in_markdown_files(tmp_path)
        assert not df_links.empty
        assert df_links.iloc[0]["file_path"] == "test.md"
        assert df_links.iloc[0]["text"] == "link text"
        assert df_links.iloc[0]["url"] == "https://example.com"

    def test_when_multiple_files_with_links_then_dataframe_with_all_links(
        self,
        tmp_path: Path,
    ):
        (tmp_path / "directory").mkdir()
        (tmp_path / "file1.md").write_text("[link1](https://example1.com)")
        (tmp_path / "directory" / "file2.md").write_text("[link2](https://example2.com)")
        (tmp_path / "directory" / "file3.md").write_text("[link3](https://example3.com)")
        df_links = search_links_in_markdown_files(tmp_path)
        assert len(df_links) == 3
        assert set(df_links["file_path"]) == {"file1.md", "directory/file2.md", "directory/file3.md"}
        assert set(df_links["text"]) == {"link1", "link2", "link3"}
        assert set(df_links["url"]) == {"https://example1.com", "https://example2.com", "https://example3.com"}

    def test_when_file_with_no_http_link_then_dataframe_with_link(
        self,
        tmp_path: Path,
    ):
        (tmp_path / "test.md").write_text("[link text](/example)")
        df_links = search_links_in_markdown_files(tmp_path)
        assert len(df_links) == 1
        assert df_links.iloc[0]["file_path"] == "test.md"
        assert df_links.iloc[0]["text"] == "link text"
        assert df_links.iloc[0]["url"] == "/example"

    def test_when_file_with_multiple_links_then_dataframe_with_all_links(
        self,
        tmp_path: Path,
    ):
        (tmp_path / "test.md").write_text("[link1](https://example1.com) and [link2](https://example2.com)")
        df_links = search_links_in_markdown_files(tmp_path)
        assert len(df_links) == 2
        assert set(df_links["text"]) == {"link1", "link2"}
        assert set(df_links["url"]) == {"https://example1.com", "https://example2.com"}

    def test_when_nested_directories_with_markdown_files_then_all_links_found(
        self,
        tmp_path: Path,
    ):
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir1" / "dir2").mkdir()
        (tmp_path / "dir1" / "file1.md").write_text("[link1](https://example1.com)")
        (tmp_path / "dir1" / "dir2" / "file2.md").write_text("[link2](https://example2.com)")
        df_links = search_links_in_markdown_files(tmp_path)
        assert len(df_links) == 2
        assert set(df_links["file_path"]) == {"dir1/file1.md", "dir1/dir2/file2.md"}
        assert set(df_links["text"]) == {"link1", "link2"}
        assert set(df_links["url"]) == {"https://example1.com", "https://example2.com"}
