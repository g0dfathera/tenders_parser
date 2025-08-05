import requests
from bs4 import BeautifulSoup
import time

OUTPUT_FILE = "tender_documents.txt"

# Your session cookie (update if it expires)
COOKIE = "SPALITE=abcdef123456v4"

SEARCH_URL = "https://tenders.procurement.gov.ge/public/library/controller.php"
DOCS_URL = "https://tenders.procurement.gov.ge/public/library/controller.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://tenders.procurement.gov.ge/public/",
    "Origin": "https://tenders.procurement.gov.ge",
    "Cookie": COOKIE
}

def get_search_payload(page: int):
    return {
        "action": "search_app",
        "app_t": "0",
        "search": "",
        "app_reg_id": "",
        "app_shems_id": "1780",
        "org_a": "",
        "app_monac_id": "0",
        "org_b": "",
        "app_particip_status_id": "0",
        "app_donor_id": "0",
        "app_status": "0",
        "app_agr_status": "20",
        "app_type": "0",
        "app_basecode": "0",
        "app_codes": "",
        "app_date_type": "1",
        "app_date_from": "",
        "app_date_tlll": "",
        "app_amount_from": "",
        "app_amount_to": "",
        "app_currency": "2",
        "app_pricelist": "0",
        "page": str(page)
    }

def extract_tender_ids(html: str):
    soup = BeautifulSoup(html, "html.parser")
    ids = []
    for row in soup.select("tr[id^=A]"):
        tid = row.get("id")
        if tid and tid.startswith("A"):
            ids.append(tid[1:])
    return ids

def fetch_documents(tender_id: str):
    params = {
        "action": "app_docs",
        "app_id": tender_id,
        "key": "undefined"
    }
    try:
        r = requests.get(DOCS_URL, headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        return r.text.strip()
    except Exception as e:
        return f"ERROR fetching tender {tender_id}: {e}"

def main():
    page = 1
    all_results = []

    while True:
        print(f"[+] Processing page {page}")
        payload = get_search_payload(page)
        r = requests.post(SEARCH_URL, data=payload, headers=HEADERS)
        if r.status_code != 200:
            print(f"[!] Failed to load page {page}")
            break

        tender_ids = extract_tender_ids(r.text)
        if not tender_ids:
            print(f"[✓] No more tenders found on page {page}. Stopping.")
            break

        for tid in tender_ids:
            print(f"  └─> Fetching documents for tender ID {tid}")
            doc_data = fetch_documents(tid)
            all_results.append(f"--- Tender ID: {tid} ---\n{doc_data}\n")
            time.sleep(0.01)  # delay

        page += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(all_results))
    print(f"\n[✓] Done. Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
