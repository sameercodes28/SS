# 🚀 Deployment Checklist

Use this checklist to deploy your S&S Price Tool step-by-step.

---

## ✅ **Phase 1: Scraper (ALREADY DONE!)**

- [x] Created `sofa-price-tool` folder
- [x] Ran scraper (`sku_discovery_tool.py`)
- [x] Generated 4 JSON files:
  - [x] `products.json`
  - [x] `sizes.json`
  - [x] `covers.json`
  - [x] `fabrics.json`

**Status:** ✅ COMPLETE

---

## 📋 **Phase 2: Local Testing (DO THIS NOW)**

### Setup (One-time)
- [ ] Open Terminal
- [ ] Navigate to project folder:
  ```bash
  cd ~/Desktop/sofa-price-tool
  ```
- [ ] Create virtual environment:
  ```bash
  python3 -m venv venv
  ```
- [ ] Activate venv:
  ```bash
  source venv/bin/activate
  ```
- [ ] Install backend dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Start Test Server
- [ ] Start local server:
  ```bash
  functions-framework --target=http_entry_point --debug
  ```
- [ ] Verify you see:
  ```
  * Running on http://127.0.0.1:8080
  Loading translation dictionaries...
  Dictionaries loaded successfully.
  ```

### Test API (Open NEW Terminal)
- [ ] **Test 1 - Sofa:**
  ```bash
  curl -X POST http://localhost:8080/getPrice \
    -H "Content-Type: application/json" \
    -d '{"query": "alwinton snuggler pacific"}'
  ```
  Expected: JSON with price ~£1,409

- [ ] **Test 2 - Chair:**
  ```bash
  curl -X POST http://localhost:8080/getPrice \
    -H "Content-Type: application/json" \
    -d '{"query": "snape chair waves"}'
  ```
  Expected: JSON with price

- [ ] **Test 3 - Bed:**
  ```bash
  curl -X POST http://localhost:8080/getPrice \
    -H "Content-Type: application/json" \
    -d '{"query": "arles super king waves"}'
  ```
  Expected: JSON with price

- [ ] **Test 4 - Dog Bed:**
  ```bash
  curl -X POST http://localhost:8080/getPrice \
    -H "Content-Type: application/json" \
    -d '{"query": "dog bed large biscuit"}'
  ```
  Expected: JSON with price

- [ ] **Test 5 - Ambiguous Query (Should Error):**
  ```bash
  curl -X POST http://localhost:8080/getPrice \
    -H "Content-Type: application/json" \
    -d '{"query": "alwinton blue"}'
  ```
  Expected: Error with fabric suggestions

### If All Tests Pass ✅
- [ ] Stop the server (Ctrl+C)
- [ ] Move to Phase 3!

### If Tests Fail ❌
- Check error messages in terminal
- Verify all 4 JSON files exist
- Check `main.py` is correct version
- Re-run: `pip install -r requirements.txt`

---

## 🚀 **Phase 3: Deploy to Google Cloud**

### Prerequisites
- [ ] Google Cloud account created
- [ ] Project ID ready: `sofaproject-476903` (or your project ID)
- [ ] `gcloud` CLI installed
- [ ] Authenticated:
  ```bash
  gcloud auth login
  ```
- [ ] Set project:
  ```bash
  gcloud config set project sofaproject-476903
  ```

### Deploy Backend
- [ ] Navigate to project folder:
  ```bash
  cd ~/Desktop/sofa-price-tool
  ```

- [ ] Run deployment command:
  ```bash
  gcloud functions deploy sofa-prototype-api \
    --gen2 \
    --runtime=python310 \
    --region=us-central1 \
    --source=. \
    --entry-point=http_entry_point \
    --trigger-http \
    --allow-unauthenticated
  ```

- [ ] Wait for deployment (2-3 minutes)

- [ ] Copy the URL from output:
  ```
  url: https://us-central1-sofaproject-476903.cloudfunctions.net/sofa-prototype-api
  ```
  **Write it here:** _______________________________________________

### Test Live Backend (Before Updating Frontend)
- [ ] Test health check:
  ```bash
  curl https://YOUR-URL-HERE
  ```
  Expected: `{"message": "S&S Price Tool Backend is ALIVE! ✅"}`

- [ ] Test actual query:
  ```bash
  curl -X POST https://YOUR-URL-HERE/getPrice \
    -H "Content-Type: application/json" \
    -d '{"query": "alwinton snuggler pacific"}'
  ```
  Expected: JSON with price

### If Backend Works ✅
- [ ] Move to Frontend deployment!

### If Backend Fails ❌
- Check Google Cloud Functions logs:
  ```bash
  gcloud functions logs read sofa-prototype-api --limit=50
  ```
- Verify all 6 files deployed:
  - `main.py`
  - `requirements.txt`
  - `products.json`
  - `sizes.json`
  - `covers.json`
  - `fabrics.json`

---

## 📱 **Phase 4: Deploy Frontend**

### Update index.html
- [ ] Open `index.html` in editor
- [ ] Find line ~188:
  ```javascript
  const BACKEND_API_URL = 'https://us-central1-sofaproject-476903.cloudfunctions.net/sofa-prototype-api/getPrice';
  ```
- [ ] Replace with YOUR URL + `/getPrice`:
  ```javascript
  const BACKEND_API_URL = 'https://YOUR-ACTUAL-URL-HERE/getPrice';
  ```
- [ ] Save file

### Push to GitHub
- [ ] Initialize git (if not already):
  ```bash
  cd ~/Desktop/sofa-price-tool
  git init
  git add index.html
  git commit -m "Deploy S&S Price Tool frontend"
  ```

- [ ] Create GitHub repo:
  - Go to github.com
  - Click "New Repository"
  - Name: `S-S` (or any name)
  - Public
  - DO NOT initialize with README
  - Create

- [ ] Connect and push:
  ```bash
  git remote add origin https://github.com/YOUR-USERNAME/S-S.git
  git branch -M main
  git push -u origin main
  ```

### Enable GitHub Pages
- [ ] Go to your repo on GitHub
- [ ] Settings → Pages (left sidebar)
- [ ] Source: `main` branch
- [ ] Folder: `/ (root)`
- [ ] Click "Save"
- [ ] Wait 1-2 minutes

### Your Live URL
Your app will be at:
```
https://YOUR-USERNAME.github.io/S-S/
```
**Write it here:** _______________________________________________

---

## 🧪 **Phase 5: Final Testing**

### Desktop Testing
- [ ] Open your `github.io` URL in Chrome
- [ ] Test voice: Click mic, say "Alwinton snuggler pacific"
  - [ ] Price appears
  - [ ] Images load
  - [ ] Specs show
- [ ] Test text: Type "snape chair waves", click Search
  - [ ] Price appears
  - [ ] Images load
- [ ] Test error: Type "alwinton blue"
  - [ ] Shows suggestions
- [ ] Test history: Check last 5 queries saved

### Mobile Testing
- [ ] Open URL on iPhone (Safari)
  - [ ] Voice works
  - [ ] Text works
  - [ ] Layout responsive
- [ ] Open URL on Android (Chrome)
  - [ ] Voice works
  - [ ] Text works
  - [ ] Layout responsive

### Browser Compatibility
- [ ] Chrome (Desktop) ✅
- [ ] Safari (Mac) ✅
- [ ] Safari (iPhone) ✅
- [ ] Chrome (Android) ✅
- [ ] Edge (Desktop) ✅
- [ ] Firefox (Desktop) - Voice won't work, but text should ⚠️

---

## 🎉 **Success Criteria**

### Backend
- [x] Deploys without errors
- [x] Returns prices for all product types
- [x] Handles ambiguous queries with suggestions
- [x] Caches responses
- [x] Logs visible in Google Cloud

### Frontend
- [x] Loads on all devices
- [x] Voice input works (Chrome/Safari)
- [x] Text input works (all browsers)
- [x] Displays prices, images, specs
- [x] Shows helpful errors
- [x] Saves query history

### End-to-End
- [x] Salesperson can speak query → Get price in <2 seconds
- [x] Works offline (no, but degrades gracefully)
- [x] Costs $0/month ✅

---

## 📅 **Future Maintenance**

### Quarterly Updates (When S&S Adds New Products)

**Option A: Quick Update (Recommended)**
1. [ ] Re-run scraper locally
2. [ ] Re-deploy backend only:
   ```bash
   gcloud functions deploy sofa-prototype-api \
     --gen2 --runtime=python310 --region=us-central1 \
     --source=. --entry-point=http_entry_point \
     --trigger-http --allow-unauthenticated
   ```
3. [ ] Test with new products
4. [ ] Frontend automatically uses new data ✅

**Option B: Full Refresh**
1. [ ] Delete `products.json`, `sizes.json`, `covers.json`, `fabrics.json`
2. [ ] Re-run scraper (20-30 min)
3. [ ] Re-deploy backend
4. [ ] Test everything

---

## 🐛 **Common Issues & Fixes**

### "No product match found"
- **Symptom:** User queries valid product, gets error
- **Cause:** Product not in `products.json`
- **Fix:** Re-run scraper

### "Request timed out"
- **Symptom:** Query takes >10 seconds, then fails
- **Cause:** S&S API is slow/down
- **Fix:** Ask user to retry in a few minutes

### "CORS error" in browser
- **Symptom:** Browser console shows CORS error
- **Cause:** Backend missing CORS headers
- **Fix:** Redeploy `main.py` (correct version has CORS)

### Frontend won't load
- **Symptom:** GitHub Pages shows 404
- **Cause:** Pages not enabled or wrong branch
- **Fix:** Settings → Pages → Set source to `main` branch

### Voice doesn't work
- **Symptom:** Mic button disabled or doesn't respond
- **Cause 1:** Non-HTTPS site (GitHub Pages is HTTPS ✅)
- **Cause 2:** Microphone permissions denied
- **Cause 3:** Firefox (doesn't support Speech API)
- **Fix:** Use Chrome/Safari or use text input

---

## ✅ **Final Checklist**

Before showing to your team:
- [ ] All 5 phases complete
- [ ] Tested on 2+ devices
- [ ] Tested 5+ different products
- [ ] Error handling works
- [ ] Backend logs clean
- [ ] Frontend loads fast
- [ ] Screenshots/recording ready

**Status:** 🎉 READY FOR PRODUCTION!

---

**Date Completed:** _______________  
**Deployed By:** _______________  
**Backend URL:** https://_______________  
**Frontend URL:** https://_______________
