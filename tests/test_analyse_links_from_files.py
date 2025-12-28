from pathlib import Path

import pandas as pd

from find_dead_links.analyse_links_from_files import analyse_links_from_files


class TestAnalyseLinksFromFiles:
    def test_no_directory(self, tmp_path: Path):
        output_path = tmp_path / "output.csv"
        unreachable_output_path = tmp_path / "unreachables.csv"
        analyse_links_from_files(
            directory=tmp_path / "nonexistent",
            output_path=output_path,
            website_domain="",
            unreachable_output_path=unreachable_output_path,
            try_again=False,
        )
        assert not output_path.exists()

    def test_analyse_links_from_files(self, tmp_path: Path):
        (tmp_path / "file1.md").write_text("[valid link](https://www.cartong.org)\n[invalid link](htp:/invalid-url)\n")
        output_path = tmp_path / "output.csv"
        unreachable_output_path = tmp_path / "unreachables.csv"
        analyse_links_from_files(
            directory=tmp_path,
            output_path=output_path,
            website_domain="",
            unreachable_output_path=unreachable_output_path,
            try_again=False,
        )
        actual = pd.read_csv(output_path)
        actual["error_message"] = actual["error_message"].fillna("")
        expected = pd.DataFrame(
            {
                "file_path": ["file1.md", "file1.md"],
                "text": ["valid link", "invalid link"],
                "url": ["https://www.cartong.org", "htp:/invalid-url"],
                "is_reachable": [True, False],
                "error_message": ["", "No connection adapters were found for 'htp:/invalid-url'"],
            }
        )
        pd.testing.assert_frame_equal(actual, expected)
        actual_unreachables = pd.read_csv(unreachable_output_path, header=None)[0].tolist()
        expected_unreachables = ["htp:/invalid-url"]
        assert actual_unreachables == expected_unreachables

    def test_try_again(self, tmp_path: Path):
        (tmp_path / "file1.md").write_text(
            "[valid link](https://www.cartong.org)\n"
            "[valid link](https://www.cartong.org/a-propos/qui-sommes-nous/)\n"
            "[invalid link](htp:/invalid-url)\n"
        )
        output_path = tmp_path / "output.csv"
        unreachable_output_path = tmp_path / "unreachables.csv"
        output_path.write_text(
            "file_path,text,url,is_reachable,error_message\n"
            "file1.md,valid link,https://www.cartong.org,True,\n"
            "file1.md,valid link,https://www.cartong.org/a-propos/qui-sommes-nous/,False,"
            "404 Client Error: Not Found for url: https://www.cartong.org/a-propos/qui-sommes-nous/\n"
            "file1.md,invalid link,htp:/invalid-url,False,No connection adapters were found for 'htp:/invalid-url'\n"
        )
        analyse_links_from_files(
            directory=tmp_path,
            output_path=output_path,
            website_domain="",
            unreachable_output_path=unreachable_output_path,
            try_again=True,
        )
        actual = pd.read_csv(output_path)
        actual["error_message"] = actual["error_message"].fillna("")
        expected = pd.DataFrame(
            {
                "file_path": ["file1.md", "file1.md", "file1.md"],
                "text": ["valid link", "valid link", "invalid link"],
                "url": [
                    "https://www.cartong.org",
                    "https://www.cartong.org/a-propos/qui-sommes-nous/",
                    "htp:/invalid-url",
                ],
                "is_reachable": [True, True, False],
                "error_message": ["", "", "No connection adapters were found for 'htp:/invalid-url'"],
            }
        )
        pd.testing.assert_frame_equal(actual, expected)
        actual_unreachables = pd.read_csv(unreachable_output_path, header=None)[0].tolist()
        expected_unreachables = ["htp:/invalid-url"]
        assert actual_unreachables == expected_unreachables
