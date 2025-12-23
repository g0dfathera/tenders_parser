# Georgian Tender Document Scraper

This Python script scrapes public tender document data from the official Georgian government procurement website (tenders.procurement.gov.ge). It parses all available pages dynamically and extracts document information related to each tender.

## Features

- Automatically iterates through all tender pages
- Extracts tender IDs and associated documents
- Saves results to a text file (`tender_documents.txt`)
- Easy to customize search parameters in the payload

## Requirements

- `Python 3+`
- `requests`
- `beautifulsoup4`

### Install Dependencies

```bash
pip install -r requirements.txt
```
Usage
Update the Cookie

Replace the value of COOKIE in the script with your valid session cookie from tenders.procurement.gov.ge:

COOKIE = "SPALITE=your_actual_cookie_here"
Run the Script
```
python main.py
```

The script will save all fetched tender document data to tender_documents.txt.

Customizing Search Filters
You can adjust the search payload inside the get_search_payload() function to:

`Filter by organization`

`Filter by date range`

`Set procurement codes` or other parameters

Example:
```
"app_codes": "44421000,",
"app_date_from": "01.01.2024",
"app_date_tlll": "05.08.2025",
```
Notes
If no tender IDs are found on a page, the script will automatically stop.

Be respectful to the host server: a small delay is added between document fetches.

If your session expires, update the cookie to continue fetching data.

## License

This script is provided as-is for educational or personal use. Not affiliated with the official government website.
