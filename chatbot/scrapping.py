from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

BASE_URL = "https://metta-lang.dev/"
visited = set()
output_file = "scraped_content.txt"

with open(output_file, "w", encoding="utf-8") as file:
    file.write("")


def scrape_page(page, url):
    page.goto(url)
    time.sleep(8)
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(["nav", "header", "footer", "aside"]):
        tag.decompose()
    for tag in soup.find_all(class_="aside"):
        tag.decompose()

    texts = []
    for element in soup.body.find_all(
        ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "code"], recursive=True
    ):
        if element.name == "p" or element.name in ["h1, h2, h3, h4, h5, h6"]:
            text_content = " ".join(element.stripped_strings)
            texts.append(text_content)
        elif element.name == "code":
            parent_div = element.find_parent("div", class_="demo-block")
            if (
                parent_div
                or element.find_parent("div", class_="language-bash")
                or element.find_parent("div", class_="language-metta")
                or element.find_parent("div", class_="language-python")
            ):
                spans = element.find_all("span", class_="line")
                code_lines = [
                    span.get_text(separator=" ", strip=True) for span in spans
                ]
                texts.append(f"Code snippet:\n" + "\n".join(code_lines))
        elif element.name == "li":
            text_content = "    - " + element.get_text(separator=" ", strip=True)
            texts.append(text_content)
        else:
            # Extract text from other tags
            text_content = element.get_text(separator="\n", strip=True)
            texts.append(text_content)

    # Join the extracted text content into a single string with newlines
    full_text = "\n".join(texts)
    return full_text, soup


def get_internal_links(soup, base_url):
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        if (
            urlparse(full_url).netloc == urlparse(base_url).netloc
            and full_url not in visited
            and "#" not in href
        ):
            links.add(full_url)
    return links


def write_to_file(url, content):
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"\n{'='*80}\nURL: {url}\n{'='*80}\n")
        file.write(content)
        file.write("\n\f\n")  # Add form feed character for page break


def main(base_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        to_visit = {base_url}

        while to_visit:
            url = to_visit.pop()
            visited.add(url)
            print(f"Scraping: {url}")
            content, soup = scrape_page(page, url)
            if soup:
                write_to_file(url, content)
                internal_links = get_internal_links(soup, base_url)
                to_visit.update(internal_links - visited)

        browser.close()


if __name__ == "__main__":
    main(BASE_URL)
