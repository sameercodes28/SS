import requests
from bs4 import BeautifulSoup
import re

# --- Setup ---
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
TEST_URL = "https://sofasandstuff.com/pillow-top-7000-pocket-spring-mattress?sku=ptskibexfoff"

def clean_keyword(name):
    name = re.sub(r'\(.*\)', '', name)
    return name.strip().lower()

print("=" * 80)
print("SIMPLE TEST: Pillow Top 7000 (4 Tensions)")
print("=" * 80)
print()

# Load page
print(f"Loading: {TEST_URL}")
response = requests.get(TEST_URL, headers=HEADERS, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')
print(f"✅ Status: {response.status_code}\n")

# Find tension button (it's a div!)
print("Looking for tension button...")
tension_button = soup.find('div', class_='btn-tension-modal')

if tension_button:
    print(f"✅ Found tension button: {tension_button.get('class')}")
    print(f"   Text: {tension_button.get_text(strip=True)[:40]}\n")
    
    # Find dropdown menu
    print("Looking for dropdown menu...")
    dropdown_menu = soup.find('div', class_='dropdown-menu', attrs={'aria-labelledby': 'dropdownMenuButton'})
    
    if dropdown_menu:
        print(f"✅ Found dropdown menu\n")
        
        # Get all items
        items = dropdown_menu.find_all('a', class_='dropdown-item')
        print(f"Found {len(items)} tension options:\n")
        
        tensions = {}
        for idx, item in enumerate(items, 1):
            tension_sku = item.get('data-coversku', '').strip().lower()
            tension_text = item.get_text(strip=True)
            keyword = clean_keyword(tension_text)
            
            print(f"  {idx}. '{tension_text}'")
            print(f"     Keyword: {keyword}")
            print(f"     SKU: {tension_sku}")
            print()
            
            tensions[keyword] = tension_sku
            tensions[tension_sku] = tension_sku
        
        print("-" * 80)
        print(f"✅ SUCCESS! Extracted {len([k for k in tensions.keys() if len(k) > 3])} tensions")
        print()
        print("Final tensions dict (keywords only):")
        for k, v in tensions.items():
            if k != v:  # Only show keywords, not SKU self-references
                print(f"  '{k}' → {v}")
        
        print()
        print("=" * 80)
        if len([k for k in tensions.keys() if len(k) > 3]) >= 4:
            print("🎉 PERFECT! All 4 tensions found!")
        else:
            print(f"⚠️  Only found {len(tensions)} tensions (expected 4)")
        print("=" * 80)
    else:
        print("❌ Dropdown menu not found")
else:
    print("❌ Tension button not found")