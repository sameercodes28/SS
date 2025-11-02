# Sofas & Stuff Voice Price Check Tool - v1

**Version:** 1.0.0
**Status:** Production Ready ✅ (Stable Release)
**Last Updated:** November 2, 2025

> **Note:** This is the v1 stable release. For v2 experimental development, see the [v2 repository](https://github.com/YOUR_USERNAME/ss-price-tool-v2).

A voice-enabled price lookup tool for Sofas & Stuff salespeople. Speak or type natural language queries (e.g., "alwinton snuggler pacific") and instantly get real-time pricing from the company's internal APIs.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ installed
- Google Cloud account (free tier)
- GitHub account (for frontend hosting)
- All 4 JSON files generated (see [Data Generation](#data-generation))

### 1. Clone & Setup
```bash
cd ~/Desktop/SS-1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test Locally
```bash
functions-framework --target=http_entry_point --debug
```

In a new terminal:
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "alwinton snuggler pacific"}'
```

Expected: JSON with price ~£1,409

### 3. Deploy Backend
```bash
gcloud functions deploy sofa-price-calculator \
  --gen2 \
  --runtime python312 \
  --entry-point http_entry_point \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-west2 \
  --timeout 60s \
  --memory 512MB
```

### 4. Update & Deploy Frontend
Edit `index.html` line 188 with your backend URL:
```javascript
const BACKEND_API_URL = 'https://YOUR-GCF-URL/getPrice';
```

Push to GitHub and enable GitHub Pages.

**Done!** Your app is live at `https://USERNAME.github.io/REPO-NAME/`

---

## 📖 Documentation

- **[README.md](README.md)** - This file (getting started)
- **[TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md)** - Complete technical deep dive
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture overview
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[docs/PRD.md](docs/PRD.md)** - Product requirements (reference)
- **[docs/PROJECT_HANDOFF.md](docs/PROJECT_HANDOFF.md)** - Project handoff doc

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Salesperson    │ (Phone/Tablet)
└────────┬────────┘
         │ "Alwinton snuggler pacific"
         ▼
┌─────────────────┐
│ Frontend (HTML) │ (GitHub Pages - Free)
│ - Voice Input   │
│ - Text Fallback │
└────────┬────────┘
         │ POST /getPrice
         ▼
┌─────────────────┐
│ Backend (GCF)   │ (Google Cloud Functions - Free)
│ - Translates    │
│ - Caches        │
│ - Routes APIs   │
└────────┬────────┘
         │
         ├──► Sofa API (sofas/chairs/mattresses)
         └──► Bed API (beds)
```

**Key Innovation:** Smart 2-API routing based on product type

---

## 📦 Project Structure

```
SS-1/
├── README.md                 ⭐ Start here
├── TECHNICAL_GUIDE.md        📚 Complete technical guide
├── ARCHITECTURE.md           🏗️  System architecture
├── CHANGELOG.md              📝 Version history
├── main.py                   🐍 Backend (deploy to GCF)
├── requirements.txt          📋 Backend dependencies
├── index.html                🌐 Frontend (deploy to GitHub Pages)
├── sku_discovery_tool.py     🔧 Data scraper (run locally)
├── requirements_scraper.txt  📋 Scraper dependencies
├── products.json             📊 Product catalog (71 KB)
├── sizes.json                📊 Size options (20 KB)
├── covers.json               📊 Cover types (4.8 KB)
├── fabrics.json              📊 Fabric data (23 MB)
└── docs/                     📁 Reference documentation
    ├── PRD.md
    └── PROJECT_HANDOFF.md
```

---

## 🎯 Features

- ✅ **Voice Input** - Tap mic and speak your query
- ✅ **Text Input** - Type query (fallback for all browsers)
- ✅ **Real-Time Pricing** - Live prices with active discounts
- ✅ **Product Images** - Image carousel for sofas/chairs
- ✅ **Specifications** - Frame, cushions, feet, etc.
- ✅ **Fabric Details** - Tier, composition, swatch image
- ✅ **Fuzzy Matching** - Handles typos and variations
- ✅ **Ambiguity Detection** - Suggests alternatives for vague queries
- ✅ **Query History** - Last 5 queries saved locally
- ✅ **Caching** - 5-minute response cache for performance

---

## 🧪 Testing

### Local Testing

**Test Sofa:**
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "alwinton snuggler pacific"}'
```

**Test Chair:**
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "snape chair waves"}'
```

**Test Bed:**
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "arles super king waves"}'
```

**Test Mattress:**
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "pillow top 7000 king extra firm"}'
```

**Test Ambiguity (should return error with suggestions):**
```bash
curl -X POST http://localhost:8080/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "alwinton blue"}'
```

### Browser Testing

Test on multiple devices:
- iPhone (Safari) - Voice + Text
- Android (Chrome) - Voice + Text
- Desktop (Chrome/Safari) - Voice + Text
- Desktop (Firefox) - Text only (no voice support)

---

## 🔄 Data Generation

### First Time Setup

Run the scraper to generate the 4 JSON files:

```bash
cd ~/Desktop/SS-1
source venv/bin/activate
pip install -r requirements_scraper.txt
python3 sku_discovery_tool.py
```

**Time:** 20-30 minutes
**Output:** products.json, sizes.json, covers.json, fabrics.json

### Quarterly Updates

Re-run the scraper when:
- S&S adds new products
- Fabric/color options change
- Quarterly maintenance (recommended)

```bash
# Re-scrape
python3 sku_discovery_tool.py

# Re-deploy backend
gcloud functions deploy sofa-price-calculator \
  --gen2 --runtime python312 --region europe-west2 \
  --source=. --entry-point=http_entry_point \
  --trigger-http --allow-unauthenticated
```

Frontend automatically uses new data - no update needed!

---

## 🐛 Troubleshooting

### "No product match found"
**Cause:** Product not in products.json
**Fix:** Re-run scraper to get latest products

### "Fabric not found"
**Cause:** Fabric/color not in fabrics.json
**Fix:** Re-run scraper OR try different color

### "Request timed out"
**Cause:** S&S API is slow/down
**Fix:** Try again in a few minutes

### "CORS error" in browser
**Cause:** Backend missing CORS headers
**Fix:** Check main.py has `Access-Control-Allow-Origin: *` (line 66-74)

### Frontend shows error connecting
**Cause:** Wrong backend URL in index.html
**Fix:** Update index.html line 188 with correct GCF URL

### Voice doesn't work
**Cause:** Browser doesn't support Speech API OR not HTTPS
**Fix:** Use Chrome/Safari OR ensure using HTTPS (GitHub Pages provides this)

---

## 💰 Cost Breakdown

| Component | Service | Tier | Cost |
|-----------|---------|------|------|
| Frontend | GitHub Pages | Free | $0/month |
| Backend | Google Cloud Functions | Free (2M requests/month) | $0/month |
| Data Storage | JSON files (26 MB total) | Free | $0/month |
| **TOTAL** | | | **$0/month** ✅ |

**Typical Usage:** 5,000-10,000 queries/month (well within free tier)

---

## 📊 Data Coverage

- **Total Products:** 210
- **Products with Full Data:** 95 (100% coverage)
- **Product Types:** 9 (sofa, chair, bed, mattress, footstool, dog_bed, sofa_bed, snuggler, corner_sofa)
- **Size Options:** 2-8 per product
- **Fabric Options:** 23MB of fabric data (thousands of combinations)
- **Mattress Tensions:** 4 options (firm, medium, extra firm, soft)

---

## 🌍 Browser Compatibility

| Browser | Voice | Text | Notes |
|---------|-------|------|-------|
| Chrome (Desktop) | ✅ | ✅ | Full support |
| Safari (Mac) | ✅ | ✅ | Full support |
| Safari (iOS) | ✅ | ✅ | Full support |
| Chrome (Android) | ✅ | ✅ | Full support |
| Edge (Chromium) | ✅ | ✅ | Full support |
| Firefox | ❌ | ✅ | No webkitSpeechRecognition |
| Samsung Internet | ❌ | ✅ | No webkitSpeechRecognition |

---

## 🔑 Key Technical Details

### How It Works

1. User speaks/types query (e.g., "alwinton snuggler pacific")
2. Frontend sends POST to backend
3. Backend translates query using 4 JSON files:
   - "alwinton" → Product SKU: `alw`, Type: `sofa`
   - "snuggler" → Size SKU: `snu`
   - (default) → Cover SKU: `fit`
   - "pacific" → Fabric SKU: `sxp`, Color SKU: `pac`
4. Backend routes to correct S&S API based on product type
5. Backend builds correct payload format
6. S&S API returns price + specs + images
7. Backend simplifies response and caches for 5 minutes
8. Frontend displays price, images, specs, fabric details

**For complete technical details, see [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md)**

### Smart 2-API Routing

S&S uses different APIs for different product types:

**Sofa API** (sofas, chairs, footstools, dog beds, mattresses):
- Endpoint: `/ProductExtend/ChangeProductSize`
- Payload: Combined SKU string (`querySku: "alwsnufitsxppac"`)
- Response: Nested JSON with images

**Bed API** (beds only):
- Endpoint: `/Category/ProductPrice`
- Payload: Component SKU parts (separate fields)
- Response: Flat JSON without images

Backend automatically selects the correct API!

---

## 🛠️ Development

### File Descriptions

**Backend Files (deploy to Google Cloud Functions):**
- `main.py` - Smart translator & API router (383 lines)
- `requirements.txt` - Backend dependencies (6 packages)
- `products.json` - Product catalog with SKUs and types
- `sizes.json` - Size options per product
- `covers.json` - Cover types per product
- `fabrics.json` - Fabric/color data per product

**Frontend Files (deploy to GitHub Pages):**
- `index.html` - Voice/text interface (478 lines)

**Local Tools (for maintenance):**
- `sku_discovery_tool.py` - Web scraper to generate JSON files (680 lines)
- `requirements_scraper.txt` - Scraper dependencies (5 packages)
- `test_mattress_scraper.py` - Test script for mattress scraping

**Documentation:**
- `README.md` - This file
- `TECHNICAL_GUIDE.md` - Complete technical deep dive
- `ARCHITECTURE.md` - System architecture
- `CHANGELOG.md` - Version history
- `docs/PRD.md` - Product requirements document
- `docs/PROJECT_HANDOFF.md` - Project handoff documentation

### Tech Stack

**Backend:**
- Python 3.12
- Google Cloud Functions (Gen 2)
- Flask (for jsonify helper)
- functions-framework
- requests (HTTP client)
- fuzzywuzzy (fuzzy string matching)
- python-Levenshtein (fuzzy matching algorithm)

**Frontend:**
- Vanilla JavaScript
- TailwindCSS (via CDN)
- webkitSpeechRecognition API
- localStorage (for query history)

**Infrastructure:**
- Google Cloud Functions (serverless backend)
- GitHub Pages (static frontend hosting)
- No database (JSON files in memory)

---

## 📈 Success Metrics

### Immediate (First Hour)
- ✅ Function deploys without errors
- ✅ Production tests pass (all product types)
- ✅ No errors in logs

### Short Term (First Week)
- Query success rate > 95%
- Response times < 2 seconds
- No 500 errors

### Long Term (Monthly)
- Data stays current (re-scrape quarterly)
- New products added as released
- Performance remains stable

---

## 🎓 Learning Resources

### For Understanding the Codebase

1. **Start with:** [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md)
   - How Google Cloud Functions work
   - How JSON files are loaded and used
   - Complete query flow with examples
   - Line-by-line code walkthrough

2. **Then read:** [ARCHITECTURE.md](ARCHITECTURE.md)
   - System architecture overview
   - API routing logic
   - Data structures
   - Design decisions

3. **Reference:** [docs/PRD.md](docs/PRD.md)
   - Original product requirements
   - Feature specifications
   - Project goals

---

## 🤝 Contributing

### Making Changes

1. Make changes locally
2. Test with `functions-framework --target=http_entry_point --debug`
3. Verify all test queries pass
4. Deploy to Google Cloud Functions
5. Test in production
6. Update CHANGELOG.md

### Adding New Features

1. Document in docs/PRD.md
2. Implement and test locally
3. Update TECHNICAL_GUIDE.md if architecture changes
4. Deploy and test in production
5. Update README.md with usage instructions

---

## 📞 Support

### Logs & Monitoring

**View Google Cloud Function logs:**
```bash
gcloud functions logs read sofa-price-calculator --limit=50
```

**View real-time logs:**
```bash
gcloud functions logs read sofa-price-calculator --follow
```

### Common Issues

See [Troubleshooting](#-troubleshooting) section above.

For technical deep dive, see [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md).

---

## 🎉 You're Ready!

Your project is production-ready. Follow the [Quick Start](#-quick-start) to deploy!

**Questions?** Check the [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md) for detailed explanations.

---

**Built with ❤️ for Sofas & Stuff**
