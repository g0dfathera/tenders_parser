import requests
from bs4 import BeautifulSoup
import time

OUTPUT_FILE = "tender_documents.txt"


SEARCH_URL = "https://tenders.procurement.gov.ge/engine/controller.php"
DOCS_URL = SEARCH_URL  

# Replace these with your actual cookie
COOKIES = {
    "SPA": "YOUR_ACTUAL_COOKIE_HERE"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://tenders.procurement.gov.ge/public/",
    "Origin": "https://tenders.procurement.gov.ge",
}

session = requests.Session()
session.headers.update(HEADERS)


def get_search_payload(page: int, custom_params=None):
    """
    Returns the payload for the search request.
    """
    payload = {
        "action": "search_app",
        "lang": "ge",  # always required
        "search": "",
        "app_reg_id": "",
        "app_shems_id": "0",
        "org_a": "",
        "app_monac_id": "0",
        "org_b": "",
        "app_particip_status_id": "0",
        "app_donor_id": "0",
        "app_status": "0",
        "app_agr_status": "0",
        "app_type": "0",
        "app_t": "0",
        "app_basecode": "0",
        "app_codes": "",
        "app_date_type": "1",
        "app_date_from": "",
        "app_date_tlll": "",
        "app_amount_from": "",
        "app_amount_to": "",
        "app_pricelist": "0",
        "app_manufacturer_id": "0",
        "app_manufacturer": "",
        "app_model_id": "0",
        "app_model": "",
        "app_currency": "2",
        "page": str(page)
    }
    if custom_params:
        payload.update(custom_params)
    return payload

def extract_tender_ids(html: str):
    soup = BeautifulSoup(html, "html.parser")
    ids = [row.get("id")[1:] for row in soup.select("tr[id^=A]") if row.get("id")]
    return ids

def fetch_documents(tender_id: str):
    payload = {
        "action": "app_docs",
        "app_id": tender_id,
        "key": "undefined",
        "lang": "ge"
    }
    try:
        r = session.post(DOCS_URL, data=payload, timeout=10)
        r.raise_for_status()
        return r.text.strip()
    except Exception as e:
        return f"ERROR fetching tender {tender_id}: {e}"


def main():
    page = 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        while True:
            print(f"[+] Processing page {page}")
            payload = get_search_payload(page)
            try:
                r = session.post(SEARCH_URL, data=payload, timeout=10)
            except Exception as e:
                print(f"[!] Failed to load page {page}: {e}")
                break

            if r.status_code != 200:
                print(f"[!] Failed page {page} | Status: {r.status_code}")
                print(r.text[:500])
                break

            tender_ids = extract_tender_ids(r.text)
            if not tender_ids:
                print(f"[✓] No more tenders found on page {page}. Stopping.")
                break

            for tid in tender_ids:
                print(f"  └─> Fetching documents for tender ID {tid}")
                doc_data = fetch_documents(tid)
                f.write(f"--- Tender ID: {tid} ---\n{doc_data}\n")
                f.flush() 
                time.sleep(0.05)  

            page += 1

    print(f"\n[✓] Done. Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

# https://tenders.procurement.gov.ge/public/?go=[ID OF THE TENDER]&lang=ge
