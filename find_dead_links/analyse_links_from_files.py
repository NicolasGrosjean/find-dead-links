import argparse
from pathlib import Path

import pandas as pd
from loguru import logger

from find_dead_links.check_url import check_url
from find_dead_links.search_links_in_file import search_links_in_markdown_files

parser = argparse.ArgumentParser(description="Analyse links in markdown files.")
parser.add_argument("directory", type=str, help="Path to the directory containing markdown files.")
parser.add_argument("output_path", type=str, help="Path to the output CSV file.")
parser.add_argument("website_domain", type=str, help="The base domain to use for relative URLs.")


def analyse_links_from_files(directory: Path, website_domain: str, output_path: Path) -> None:
    """Analyse links found in markdown files within the given directory."""
    if not directory.is_dir():
        logger.error(f"The provided directory does not exist or is not a directory: {directory}")
        return
    df_links = search_links_in_markdown_files(directory)
    logger.info(f"Found {len(df_links)} links in markdown files.")
    df_urls = pd.DataFrame(df_links["url"].unique(), columns=["url"])
    logger.info(f"Checking reachability of {len(df_urls)} unique URLs.")
    df_urls["is_reachable"], df_urls["error_message"] = zip(
        *df_urls["url"].map(lambda url: check_url(url, website_domain)), strict=True
    )
    df_links = df_links.merge(df_urls, on="url", how="left")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_links.to_csv(output_path, index=False)
    logger.info(f"Analysis complete. Results saved to {output_path}")


if __name__ == "__main__":
    args = parser.parse_args()
    analyse_links_from_files(
        directory=Path(args.directory),
        output_path=Path(args.output_path),
        website_domain=args.website_domain,
    )
