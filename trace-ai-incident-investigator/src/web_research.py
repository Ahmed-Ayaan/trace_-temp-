import os
from pathlib import Path
import requests
from dotenv import load_dotenv

# project configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
API_KEY = os.getenv("TINYFISH_API_KEY")
SEARCH_URL = "https://api.search.tinyfish.ai"
FETCH_URL = "https://api.fetch.tinyfish.ai"

def search_web(query):
    if not API_KEY:
        raise RuntimeError("TINYFISH_API_KEY is missing from .env")
    response = requests.get(
        SEARCH_URL,
        headers={"X-API-Key": API_KEY},
        params={"query": query,
            "location": "IN",
            "language": "en"},
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

def fetch_pages(urls):
    if not API_KEY:
        raise RuntimeError("TINYFISH_API_KEY is missing from .env")
    if not urls:
        return []
    response = requests.post(
        FETCH_URL,
        headers={"X-API-Key": API_KEY,
            "Content-Type": "application/json"},
        json={"urls": urls[:3],
            "format": "markdown"},
        timeout=90
    )
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])

def build_search_query(incident):
    technology = incident.get("technology", {})
    context = incident.get("investigation_context", {})
    application = technology.get("application", "")
    database = technology.get("database", "")
    dependency = technology.get("database_image", "")
    version = technology.get("current_version", "")
    symptoms = context.get("symptoms", [])
    symptom_text = " ".join(symptoms[:2])
    query_parts = [application,
        database,
        dependency,
        version,
        symptom_text,
        "known issues"]
    return " ".join(part for part in query_parts if part)

def research_incident(incident):
    query = build_search_query(incident)
    print("\nTRACE EXTERNAL RESEARCH")
    print("=" * 60)
    print(f"Search query: {query}")
    search_results = search_web(query)
    if not search_results:
        return {"query": query,
            "sources": [],
            "message": "No search results were returned."}
    candidates = []
    for result in search_results:
        url = result.get("url")
        if not url:
            continue
        candidates.append({"title": result.get("title", ""),
            "url": url,
            "snippet": result.get("snippet", "")})
        if len(candidates) == 3:
            break
    if not candidates:
        return {"query": query,
            "sources": [],
            "message": "No usable URLs were returned."}
    print(f"\nCandidate webpages: {len(candidates)}")
    for index, candidate in enumerate(candidates,start=1):
        print(f"{index}. {candidate['title']}")
        print(f"   {candidate['url']}")
    urls = [candidate["url"] for candidate in candidates]
    fetched_pages = fetch_pages(urls)
    candidates_by_url = {candidate["url"]: candidate for candidate in candidates}
    sources = []
    for page in fetched_pages:
        url = page.get("url", "")
        candidate = candidates_by_url.get(url, {})
        sources.append({
            "title": page.get("title",candidate.get("title", "")),
            "url": page.get("url",candidate.get("url", "")),
            "snippet": candidate.get("snippet", ""),
            "content": page.get("text", "")
        })
    return {"query": query,
        "sources": sources,
        "message": ("External research completed." if sources
            else "No readable webpage content was returned.")}

def main():
    incident_path = (PROJECT_ROOT / "data" / "incidents.json")
    import json
    with open(incident_path,"r",encoding="utf-8") as file:
        incident = json.load(file)
    try:
        result = research_incident(incident)
        print("\nRESEARCH RESULTS")
        print("=" * 60)
        print(result["message"])
        for index, source in enumerate(result["sources"],start=1):
            print(f"\nSOURCE {index}")
            print("-" * 60)
            print(f"Title: {source['title']}")
            print(f"URL: {source['url']}")
            content = source["content"]
            if content:
                print("\nRetrieved content:")
                print(content[:2000])
            else:
                print("\nNo readable content returned.")
    except requests.RequestException as error:
        print(f"TinyFish API request failed: {error}")
    except (RuntimeError, ValueError) as error:
        print(f"Research failed: {error}")

if __name__ == "__main__":
    main()
