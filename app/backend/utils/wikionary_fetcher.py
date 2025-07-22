import json
import re
import requests
from bs4 import BeautifulSoup

CATEGORIES = [
    "Aussprache",
    "Herkunft",
    "Koseformen",
    "Namensvarianten",
    "Weibliche Namensvarianten",
    "Männliche Namensvarianten",
    "Bekannte Namensträger",
    "Alternative Schreibweisen",
    "Abkürzungen",
]


def clean_text(text):
    text = re.sub(r" ?\[ ?\d+ ?\]", "", text)
    text = re.sub(r" ?\[.*?Quellen.*?\]", "", text)
    return text.strip()


def extract_name_info(name):
    url = f"https://de.wiktionary.org/wiki/{name}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    section = soup.find(
        "h3", id=lambda x: x and x.startswith("Substantiv,_") and "_Vorname" in x
    )
    if not section:
        return None

    section = section.find_parent("section")
    data = {}

    for cat in CATEGORIES:
        if cat == "Aussprache":
            audio = section.select_one("a[href$='.ogg']")
            if audio:
                data["aussprache_link"] = "https:" + audio["href"]

            ipa = section.select_one("span.ipa")
            if ipa:
                data["ipa"] = ipa.text.strip()

            continue

        heading = section.find(
            "p", string=lambda x: x and x.strip().startswith(cat + ":")
        )
        if heading:
            dl = heading.find_next_sibling("dl")
            if not dl:
                continue

            entries = [
                clean_text(dd.get_text(" ", strip=True)) for dd in dl.find_all("dd")
            ]

            if cat == "Abkürzungen":
                entries = [e for e in entries if len(e.replace(".", "").strip()) > 2]

            if entries:
                data[cat] = "\n".join(entries)

    return data


# Example
if __name__ == "__main__":
    result = extract_name_info("Felix")
    if result:
        print("Information for 'Felix':")
        print(json.dumps(result, ensure_ascii=False, indent=2))
