
import urllib.request
import xml.etree.ElementTree as ET


def fetch_research_paper(paper_id):

    url = (
        "https://export.arxiv.org/api/query?id_list="
        + paper_id
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "LessonContentGenerator/1.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)

    namespace = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    entry = root.find("atom:entry", namespace)

    if entry is None:
        return None

    title = entry.findtext("atom:title", namespaces=namespace)
    summary = entry.findtext("atom:summary", namespaces=namespace)

    return {
        "title": title.strip() if title else "",
        "summary": summary.strip() if summary else "",
        "source": f"https://arxiv.org/abs/{paper_id}"
    }
