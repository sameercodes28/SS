# Final Deployment Checklist - November 1, 2025

## ✅ SYSTEM STATUS: READY FOR PRODUCTION

All tests passing. All bugs fixed. Ready to deploy.

---

## 📦 FILES TO DEPLOY (6 Files Required)

Copy these files to deployment directory:

```bash
cd ~/Desktop/sofa-price-tool

# Verify all files exist and are not empty:
ls -lh main.py requirements.txt *.json

# Should see:
# main.py           (~12 KB)
# requirements.txt  (~1 KB)
# products.json     (~500 KB)
# sizes.json        (~50 KB)
# covers.json       (~15 KB)
# fabrics.json      (~2 MB)
```

---

## 1️⃣ main.py - Backend (MODIFIED)

**Status:** ✅ Fixed for mattress support  
**Size:** ~12 KB  
**Last modified:** Today (November 1, 2025)  

**Key changes from original:**
- Added mattress routing to SOFA_API (line ~255)
- Builds correct query SKU for mattresses: `product + size + tension + off + off`
- Keeps bed routing separate

**Test command:**
```bash
# Start local server
functions-framework --target=http_entry_point --debug

# Test (in new terminal)
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "pillow top 7000 king extra firm"}'
```

**Expected:** Returns price ~£2,049

---

## 2️⃣ requirements.txt - Dependencies (UNCHANGED)

**Status:** ✅ No changes needed  
**Size:** ~200 bytes  

**Contents:**
```
beautifulsoup4>=4.12.0
Flask>=2.0
functions-framework>=3.0
requests>=2.31.0
urllib3>=1.26.0
fuzzywuzzy>=0.18.0
python-Levenshtein>=0.20.0
```

---

## 3️⃣ products.json - Product Catalog (MODIFIED)

**Status:** ✅ Fixed ambiguous keywords  
**Size:** ~500 KB  
**Entries:** 202 products + keyword aliases = ~300 entries  

**Key changes:**
- ❌ Removed: `"pillow"` (ambiguous)
- ❌ Removed: `"pillow mattress"` (ambiguous)
- ✅ Added: `"pillow top 4000"` → ptf
- ✅ Added: `"pillow top 7000"` → pts
- ✅ Added: `"pillow 4000"` → ptf
- ✅ Added: `"pillow 7000"` → pts
- ✅ Added: `"pillowtop 4000"` → ptf
- ✅ Added: `"pillowtop 7000"` → pts

**Verify:**
```bash
grep -c "pillow" products.json
# Should show ~10 (specific keywords only, no generic "pillow")

grep "\"pillow\":" products.json
# Should return nothing (removed ambiguous keyword)
```

---

## 4️⃣ sizes.json - Size Options (MODIFIED)

**Status:** ✅ Added shortened keywords  
**Size:** ~50 KB  

**Key changes for mattresses:**
```json
{
  "pts": {
    "super king mattress": "skb",
    "super king": "skb",  // ← ADDED
    "skb": "skb",
    "king mattress": "kib",
    "king": "kib",  // ← ADDED
    "kib": "kib",
    "double mattress": "dbb",
    "double": "dbb",  // ← ADDED
    "dbb": "dbb",
    "single mattress": "sib",
    "single": "sib",  // ← ADDED
    "sib": "sib"
  }
}
```

**Verify:**
```bash
python3 -c "import json; s=json.load(open('sizes.json')); print('king' in s['pts'])"
# Should print: True
```

---

## 5️⃣ covers.json - Cover Types (MODIFIED)

**Status:** ✅ Fixed mattress covers  
**Size:** ~15 KB  

**Key changes for mattresses:**
```json
{
  "pts": {
    "off": "off"  // ← FIXED (was "fir": "fir")
  }
}
```

**Before (WRONG):**
```json
{
  "pts": {
    "fir": "fir"  // Tension code, not cover type!
  }
}
```

**Verify:**
```bash
python3 -c "import json; c=json.load(open('covers.json')); print(c['pts'])"
# Should print: {'off': 'off'}
```

---

## 6️⃣ fabrics.json - Fabrics/Tensions (MODIFIED)

**Status:** ✅ Fixed tension format  
**Size:** ~2 MB  

**Key changes for mattresses:**

**Before (WRONG) - String format:**
```json
{
  "pts": {
    "extra firm": "exf",
    "exf": "exf"
  }
}
```

**After (CORRECT) - Dictionary format:**
```json
{
  "pts": {
    "extra firm": {
      "fabric_sku": "exf",
      "color_sku": "exf",
      "fabric_name": "Extra Firm",
      "color_name": "Extra Firm",
      "collection": "Mattress Firmness",
      "tier": "Standard",
      "desc": "Extra Firm firmness mattress",
      "swatch_url": "",
      "fabric_id": "",
      "color_id": ""
    },
    "exf": {
      "fabric_sku": "exf",
      ...
    }
  }
}
```

**Verify:**
```bash
python3 -c "import json; f=json.load(open('fabrics.json')); print(type(f['pts']['extra firm']))"
# Should print: <class 'dict'>  (not <class 'str'>)
```

---

## 🧪 PRE-DEPLOYMENT TESTS

Run these **BEFORE** deploying:

### Test 1: Sofa
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "alwinton snuggler pacific"}'
```
**Expected:** Price ~£1,958 ✅

### Test 2: Mattress
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "pillow top 7000 king extra firm"}'
```
**Expected:** Price ~£2,049 ✅

### Test 3: Chair
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "snape chair waves"}'
```
**Expected:** Price ~£1,431 ✅

**All three must pass before deploying!**

---

## 🚀 DEPLOYMENT COMMAND

```bash
cd ~/Desktop/sofa-price-tool

gcloud functions deploy sofa-price-calculator \
  --gen2 \
  --runtime python312 \
  --entry-point http_entry_point \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west2 \
  --timeout 60s \
  --memory 512MB \
  --max-instances 10
```

**Time:** ~3 minutes  
**Output:** Production URL

---

## ✅ POST-DEPLOYMENT VERIFICATION

After deployment completes, test production:

```bash
# Replace YOUR_URL with actual URL from deployment
PROD_URL="https://europe-west2-PROJECT.cloudfunctions.net/sofa-price-calculator"

# Test 1
curl -X POST $PROD_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "alwinton snuggler pacific"}'

# Test 2
curl -X POST $PROD_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "pillow top 7000 king extra firm"}'

# Test 3
curl -X POST $PROD_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "snape chair waves"}'
```

**All three must return prices in production!**

---

## 📱 UPDATE iOS APP

In your iOS app, update the endpoint:

```swift
// Change from:
let apiURL = "http://localhost:8080/getPrice"

// To:
let apiURL = "https://europe-west2-YOUR_PROJECT.cloudfunctions.net/sofa-price-calculator/getPrice"
```

Test in iOS app:
1. Search "alwinton snuggler pacific" → Should show price
2. Search "pillow top 7000 king extra firm" → Should show price
3. Search "snape chair waves" → Should show price

---

## 📊 FILES NOT NEEDED FOR DEPLOYMENT

These stay local (for maintenance/debugging):

```
❌ sku_discovery_tool_WORKING.py  (scraper - run locally only)
❌ fix_mattress_tensions.py       (one-time fix script)
❌ fix_mattress_mappings.py       (one-time fix script)
❌ fix_pillow_keywords.py         (one-time fix script)
❌ remove_ambiguous_keywords.py   (one-time fix script)
❌ debug_*.py                     (diagnostic scripts)
❌ test_*.py                      (testing scripts)
❌ verify_*.py                    (verification scripts)
❌ check_*.py                     (checking scripts)
```

**Only deploy the 6 core files!**

---

## 🔄 FUTURE RE-SCRAPING

When you need to update data (monthly recommended):

```bash
cd ~/Desktop/sofa-price-tool
source venv/bin/activate

# 1. Re-scrape (30 min)
python3 sku_discovery_tool_WORKING.py

# 2. Backup old files
cp products.json products.json.backup
cp sizes.json sizes.json.backup
cp covers.json covers.json.backup
cp fabrics.json fabrics.json.backup

# 3. Fix any issues (if needed)
python3 fix_mattress_tensions.py
python3 fix_mattress_mappings.py
python3 remove_ambiguous_keywords.py

# 4. Test locally
functions-framework --target=http_entry_point --debug
# Run all 3 test queries

# 5. Deploy
gcloud functions deploy sofa-price-calculator ...

# 6. Test production
curl -X POST PROD_URL/getPrice ...
```

---

## ⚠️ CRITICAL NOTES

1. **Don't modify JSON files manually** - use the fix scripts or re-scrape
2. **Always test locally first** - never deploy untested changes
3. **Backup before re-scraping** - in case something breaks
4. **Check logs after deployment** - watch for errors in first hour
5. **Monitor query patterns** - identify products that don't match

---

## 🎯 DEPLOYMENT CHECKLIST

Before clicking deploy:

- [ ] All 6 files present and not empty
- [ ] Local tests pass (3/3)
- [ ] main.py has mattress support
- [ ] products.json has specific keywords (no "pillow" alone)
- [ ] sizes.json has shortened keywords ("king" not just "king mattress")
- [ ] covers.json has "off" for mattresses (not "fir")
- [ ] fabrics.json has dictionaries for mattresses (not strings)
- [ ] Google Cloud SDK installed and authenticated
- [ ] Project ID set correctly
- [ ] Required APIs enabled

**If all checked, proceed with deployment!**

---

## 📈 SUCCESS METRICS

**Immediate (First Hour):**
- [ ] Function deploys without errors
- [ ] Production tests pass (3/3)
- [ ] iOS app connects successfully
- [ ] No errors in logs

**Short Term (First Week):**
- [ ] All user queries return results
- [ ] Response times < 2 seconds
- [ ] No 500 errors
- [ ] Query success rate > 95%

**Long Term (Monthly):**
- [ ] Data stays current (re-scrape monthly)
- [ ] New products added as S&S releases them
- [ ] Keywords refined based on usage patterns
- [ ] Performance remains stable

---

## 🎉 FINAL STATUS

**System State:** Production Ready  
**Test Results:** 3/3 Passing  
**Bugs Fixed:** 7 Major Issues Resolved  
**Next Action:** Deploy to Google Cloud

**Estimated deployment time:** 15 minutes  
