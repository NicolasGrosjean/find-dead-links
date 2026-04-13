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
parser.add_argument("--try-again", action="store_true", help="Retry checking URLs that were previously unreachable.")
parser.add_argument("--unreachable-output", type=str, default="unreachables.csv", help="Path to save unreachable URLs.")


def analyse_links_from_files(
    directory: Path, website_domain: str, output_path: Path, unreachable_output_path: Path, *, try_again: bool
) -> None:
    """Analyse links found in markdown files within the given directory."""
    if not directory.is_dir():
        logger.error(f"The provided directory does not exist or is not a directory: {directory}")
        return
    if try_again and output_path.exists():
        df_links = pd.read_csv(output_path)
        unreachable_urls = df_links.loc[~df_links["is_reachable"], "url"].unique()
        logger.info(f"Retrying {len(unreachable_urls)} previously unreachable URLs.")
        df_urls = pd.DataFrame(unreachable_urls, columns=["url"])
        df_urls["is_reachable"], df_urls["error_message"] = zip(
            *df_urls["url"].map(lambda url: _check_non_archive_url(url, website_domain)), strict=True
        )
        logger.info(f"{(~df_urls['is_reachable']).sum()} URLs are still not reachable after retrying.")
        # Merge updated results back into the original links dataframe
        df_links = df_links.drop(columns=["is_reachable", "error_message"]).merge(df_urls, on="url", how="left")
        # The rows with URLs that were not retried were reachable without issues
        df_links = df_links.fillna({"is_reachable": True, "error_message": ""})
    else:
        df_links = search_links_in_markdown_files(directory)
        logger.info(f"Found {len(df_links)} links in markdown files.")
        df_urls = pd.DataFrame(df_links["url"].unique(), columns=["url"])
        logger.info(f"Checking reachability of {len(df_urls)} unique URLs.")
        df_urls["is_reachable"], df_urls["error_message"] = zip(
            *df_urls["url"].map(lambda url: _check_non_archive_url(url, website_domain)), strict=True
        )
        logger.info(f"{(~df_urls['is_reachable']).sum()} URLs are not reachable after retrying.")
        df_links = df_links.merge(df_urls, on="url", how="left")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_links.drop_duplicates().to_csv(output_path, index=False)
    logger.info(f"Analysis complete. Results saved to {output_path}.")
    unreachables_url = df_links[~df_links["is_reachable"]]["url"].unique()
    for i in range(len(unreachables_url)):
        if unreachables_url[i].startswith("/"):
            unreachables_url[i] = website_domain.rstrip("/") + unreachables_url[i]
    pd.DataFrame(sorted(unreachables_url)).to_csv(unreachable_output_path, index=False, header=False)
    logger.info(f"Unreachable URLs saved to {unreachable_output_path}.")


def _check_non_archive_url(
    url: str, website_domain: str, sleep_time: float = 0.1, timeout: int = 5
) -> tuple[bool, str]:
    if url.startswith("https://web.archive.org"):
        return True, ""
    return check_url(url, website_domain, sleep_time, timeout)


if __name__ == "__main__":
    args = parser.parse_args()
    analyse_links_from_files(
        directory=Path(args.directory),
        output_path=Path(args.output_path),
        website_domain=args.website_domain,
        unreachable_output_path=Path(args.unreachable_output),
        try_again=args.try_again,
    )
