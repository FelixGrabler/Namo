import json
import re
import requests
from bs4 import BeautifulSoup


def clean_text(text):
    """Remove citation markers and other unwanted elements from text"""
    text = re.sub(r" ?\[ ?\d+ ?\]", "", text)
    text = re.sub(r" ?\[.*?Quellen.*?\]", "", text)
    text = re.sub(r"\[.*?\]", "", text)  # Remove all square bracket references

    # Remove "Hauptartikel" references followed by line breaks
    text = re.sub(r"→ Hauptartikel:.*?\n+", "", text, flags=re.DOTALL)

    return text.strip()


def extract_herkunft_bedeutung_section(soup):
    """Extract the 'Herkunft und Bedeutung' section content"""
    # Find the heading
    heading = soup.find("h2", id="Herkunft_und_Bedeutung")
    if not heading:
        return None

    # Get the parent div that contains the heading
    heading_div = heading.find_parent("div", class_="mw-heading")
    if not heading_div:
        return None

    # Collect all content after the heading until the next heading
    content_parts = []
    current = heading_div.next_sibling

    while current:
        if current.name == "div" and "mw-heading" in (current.get("class") or []):
            # Found another heading, stop collecting
            break
        elif current.name == "p":
            # Collect paragraph text
            text = clean_text(current.get_text())
            if text:
                content_parts.append(text)
        elif current.name == "ul":
            # Collect list items
            for li in current.find_all("li"):
                text = clean_text(li.get_text())
                if text:
                    content_parts.append(f"• {text}")

        current = current.next_sibling

    return "\n\n".join(content_parts) if content_parts else None


def extract_name_info(name):
    """Extract name information from German Wikipedia"""
    # Try both URL patterns
    urls = [
        f"https://de.wikipedia.org/wiki/{name}#Herkunft_und_Bedeutung",
        f"https://de.wikipedia.org/wiki/{name}_(Name)#Herkunft_und_Bedeutung",
        f"https://de.wikipedia.org/wiki/{name}_(Vorname)#Herkunft_und_Bedeutung",
    ]

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code != 200:
                continue

            # Check if the article exists
            if "Dieser Artikel existiert nicht." in response.text:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the "Herkunft und Bedeutung" section
            content = extract_herkunft_bedeutung_section(soup)

            if content:
                return {"Herkunft": content, "source_url": url}

        except requests.RequestException as e:
            print(f"Request error fetching {url}: {str(e)}")
            continue
        except ValueError as e:
            print(f"Parsing error fetching {url}: {str(e)}")
            continue

    return None


# Example
if __name__ == "__main__":
    result = extract_name_info("Matteo")
    if result:
        print("Information for 'Matteo':")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("No information found for 'Matteo'")
