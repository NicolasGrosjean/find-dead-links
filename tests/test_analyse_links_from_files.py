from pathlib import Path

import pandas as pd

from find_dead_links.analyse_links_from_files import analyse_links_from_files


class TestAnalyseLinksFromFiles:
    def test_analyse_links_from_files(self, tmp_path: Path):
        (tmp_path / "file1.md").write_text("[valid link](https://www.cartong.org)\n[invalid link](htp:/invalid-url)\n")
        output_path = tmp_path / "output.csv"
        analyse_links_from_files(directory=tmp_path, output_path=output_path, website_domain="")
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
