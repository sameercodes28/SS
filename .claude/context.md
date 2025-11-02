# Claude Context - Sofas & Stuff Price Tool

**Last Updated:** 2025-11-02
**Current Version:** v1.0.0
**Project Status:** Production Ready ✅

> **Purpose:** This file helps Claude (or any LLM) quickly understand the project state, recent changes, and ongoing work. Update this file at the end of each session.

> **Note:** Claude Code automatically reads this file via `.claude/instructions.md` - no manual prompting needed!

---

## 📋 Quick Project Summary

**What is this?**
A voice-enabled price lookup tool for Sofas & Stuff salespeople. Users speak/type queries like "alwinton snuggler pacific" and get real-time pricing from S&S internal APIs.

**Architecture:**
```
Frontend (index.html) → Backend (main.py on GCF) → S&S APIs (2 different endpoints)
GitHub Pages (free)     Google Cloud Functions      Sofa API + Bed API
```

**Key Innovation:** Smart 2-API routing system that automatically selects the correct S&S API based on product type.

**Current Deployment:**
- Backend: `https://europe-west2-sofaproject-476903.cloudfunctions.net/sofa-price-calculator`
- Frontend: Ready for GitHub Pages (URL needs updating)

---

## 🎯 Current State

### What's Working ✅
- [x] Backend deployed to Google Cloud Functions
- [x] 4 JSON files generated (products, sizes, covers, fabrics)
- [x] 210 products with 95 having complete data
- [x] Natural language query processing
- [x] Fuzzy matching for typos
- [x] Smart 2-API routing (Sofa API vs Bed API)
- [x] Mattress support with tension options
- [x] Caching system (5-min TTL)
- [x] Error handling with helpful messages
- [x] Documentation consolidated (11 → 5 files)

### What Needs Work ⚠️
- [ ] Frontend deployment to GitHub Pages (pending)
- [ ] Production testing on multiple devices
- [ ] User acceptance testing

### Known Issues 🐛
- None currently (fabric swatch bug fixed on 2025-11-02)

---

## 📂 Important File Locations

### Core Backend Files (Deploy to GCF)
- `main.py` - Backend translator (383 lines)
- `requirements.txt` - Backend dependencies
- `products.json` - Product catalog (71 KB)
- `sizes.json` - Size options (20 KB)
- `covers.json` - Cover types (4.8 KB)
- `fabrics.json` - Fabric data (23 MB)

### Frontend Files
- `index.html` - Voice/text interface (478 lines)
  - **Line 188:** Backend API URL (needs updating before deploy)

### Data Generation
- `sku_discovery_tool.py` - Web scraper (680 lines)
- `requirements_scraper.txt` - Scraper dependencies

### Documentation
- `README.md` - Getting started guide (main entry point)
- `TECHNICAL_GUIDE.md` - Complete technical deep dive
- `ARCHITECTURE.md` - System architecture overview
- `CHANGELOG.md` - Version history
- `docs/PRD.md` - Product requirements

### AI Context
- `.claude/context.md` - This file (for LLM session continuity)

---

## 🔧 Recent Changes

### Session: 2025-11-02 (Documentation Consolidation)

**Changes Made:**
1. ✅ Created comprehensive TECHNICAL_GUIDE.md
   - Explains how Google Cloud Functions work
   - Shows how JSON files are loaded into RAM
   - Complete query flow with examples
   - Line-by-line code walkthrough

2. ✅ Consolidated documentation (11 → 5 files)
   - Deleted: START_HERE.md, START_HERE_NOW.md, DEPLOYMENT_CHECKLIST.md, FINAL_DEPLOYMENT_CHECKLIST.md, implementation_guide.md, WHATS_CHANGED.md, PROJECT_HANDOFF.md
   - Created: New README.md, TECHNICAL_GUIDE.md, CHANGELOG.md
   - Moved: PRD.md → docs/PRD.md
   - Kept: ARCHITECTURE.md

3. ✅ Created this context file (.claude/context.md)

**Files Modified:**
- Created: `.claude/context.md`
- Created: `TECHNICAL_GUIDE.md` (31 KB)
- Created: `CHANGELOG.md` (1.8 KB)
- Replaced: `README.md` (new consolidated version)
- Moved: `docs/PRD.md`, `docs/PROJECT_HANDOFF.md` (then deleted handoff)
- Deleted: 9 redundant markdown files

**Decisions Made:**
- Documentation structure: Main docs in root, reference docs in `/docs`
- TECHNICAL_GUIDE.md is the go-to for understanding how everything works
- README.md is the single starting point for new users

---

### Session: 2025-11-01 (Initial Development)

**Changes Made:**
1. Fixed fabric swatch URL bug (main.py:344)
   - Changed from `fabric_match_data.get('swatch')` to `fabric_match_data.get('swatch_url')`
2. Backend deployed to Google Cloud Functions
3. Generated 4 JSON files from scraper
4. Validated mattress support

---

## 🎯 Ongoing Tasks

### High Priority
- [ ] Deploy frontend to GitHub Pages
- [ ] Update index.html line 188 with production backend URL
- [ ] Production testing on iPhone, Android, Desktop
- [ ] User acceptance testing with salespeople

### Medium Priority
- [ ] Monitor backend logs for first week
- [ ] Document any edge cases discovered
- [ ] Create user training guide

### Low Priority
- [ ] Consider adding analytics
- [ ] Consider authentication for internal use
- [ ] Optimize cache TTL based on usage patterns

---

## 💡 Important Context for LLMs

### Critical Design Decisions

1. **Why Google Cloud Functions?**
   - Serverless (no maintenance)
   - Free tier generous (2M requests/month)
   - HTTPS included
   - Auto-scaling

2. **Why 2 Different APIs?**
   - S&S uses different API endpoints for different product types
   - Sofa API: `/ProductExtend/ChangeProductSize` (sofas, chairs, mattresses)
   - Bed API: `/Category/ProductPrice` (beds only)
   - Backend automatically routes based on product type

3. **Why JSON Files Instead of Database?**
   - Fast lookups (in-memory dictionaries)
   - No database cost
   - Easy to version control
   - Simple to update (re-run scraper)

4. **Why Load JSON Files at Startup?**
   - GCF containers persist for ~15 minutes
   - Loading once per container is efficient
   - 26 MB fits easily in 512 MB memory
   - All requests share the same loaded data

### Common Gotchas

1. **index.html Line 188 MUST be updated** before frontend deployment
   - Default: placeholder URL
   - Required: actual GCF URL from deployment

2. **Mattresses are special:**
   - Use tensions (firm, medium, etc.) instead of fabrics
   - Route to Sofa API (not Bed API)
   - SKU format: `product + size + tension + off + off`

3. **Fabric swatch bug (FIXED):**
   - JSON uses `swatch_url` not `swatch`
   - main.py:344 now correctly references `swatch_url`

4. **CORS is critical:**
   - Backend must return `Access-Control-Allow-Origin: *`
   - Without it, frontend can't call backend
   - Already implemented in main.py lines 63-74

### Code Reference Points

**main.py Key Lines:**
- Lines 48-55: JSON files loaded into RAM (happens once per container)
- Lines 166-180: Product lookup
- Lines 183-195: Size lookup
- Lines 198-209: Cover lookup
- Lines 212-231: Fabric lookup
- Lines 257-285: API routing logic (Sofa vs Bed)
- Line 344: Fabric swatch URL (was buggy, now fixed)
- Lines 363-383: HTTP entry point

**index.html Key Lines:**
- Line 188: Backend API URL (UPDATE THIS!)
- Lines 140-180: Voice recognition
- Lines 188-220: API call to backend
- Lines 250-320: Display results

---

## 🗂️ Data Structures Quick Reference

### products.json
```json
{
  "alwinton": {
    "sku": "alw",
    "type": "sofa",  // ← Used for API routing!
    "full_name": "Alwinton 3 Seater Sofa"
  }
}
```

### sizes.json (nested by product SKU)
```json
{
  "alw": {
    "snuggler": "snu",
    "3 seater": "3se"
  }
}
```

### covers.json (nested by product SKU)
```json
{
  "alw": {
    "fitted": "fit",
    "loose": "lse"
  }
}
```

### fabrics.json (nested by product SKU)
```json
{
  "alw": {
    "pacific": {
      "fabric_sku": "sxp",
      "color_sku": "pac",
      "swatch_url": "https://..."  // ← Note: swatch_url not swatch!
    }
  }
}
```

---

## 🧪 Test Queries

Use these to verify the system works:

**Sofa:**
```bash
curl -X POST $BACKEND_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "alwinton snuggler pacific"}'
```
Expected: £1,409

**Chair:**
```bash
curl -X POST $BACKEND_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "snape chair waves"}'
```

**Bed:**
```bash
curl -X POST $BACKEND_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "arles super king waves"}'
```

**Mattress:**
```bash
curl -X POST $BACKEND_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "pillow top 7000 king extra firm"}'
```

**Ambiguity (should error with suggestions):**
```bash
curl -X POST $BACKEND_URL/getPrice \
  -H "Content-Type: application/json" \
  -d '{"query": "alwinton blue"}'
```

---

## 🚨 If Something Goes Wrong

### Backend Issues
1. Check logs: `gcloud functions logs read sofa-price-calculator --limit=50`
2. Verify all 6 files deployed (main.py + requirements.txt + 4 JSONs)
3. Test health check: `curl https://YOUR-URL/`

### Frontend Issues
1. Check browser console for errors
2. Verify index.html line 188 has correct URL
3. Test backend directly with curl first
4. Check CORS headers in network tab

### Data Issues
1. Re-run scraper: `python3 sku_discovery_tool.py`
2. Re-deploy backend with new JSON files
3. Frontend automatically uses new data

---

## 📝 Session Checklist (For Next Claude Session)

When starting a new session:
1. [ ] Read this context file first
2. [ ] Check CHANGELOG.md for recent changes
3. [ ] Review ongoing tasks above
4. [ ] Check if any files have been modified
5. [ ] Update this file at end of session

When ending a session:
1. [ ] Update "Recent Changes" section with what you did
2. [ ] Update "Ongoing Tasks" section
3. [ ] Update "Current State" if needed
4. [ ] Add any new gotchas to "Common Gotchas"
5. [ ] Update "Last Updated" date at top

---

## 🎓 Learning Resources

For new LLMs joining the project:

1. **Quick Start:** Read this file first (you're here!)
2. **User Guide:** Read README.md (13 KB)
3. **Technical Deep Dive:** Read TECHNICAL_GUIDE.md (31 KB) - explains everything
4. **Architecture:** Read ARCHITECTURE.md (15 KB)
5. **Requirements:** Read docs/PRD.md (6.5 KB)

---

## 🔗 External References

- **Google Cloud Project:** `sofaproject-476903`
- **GCF Region:** `europe-west2`
- **S&S Website:** https://sofasandstuff.com
- **Sofa API Endpoint:** https://sofasandstuff.com/ProductExtend/ChangeProductSize
- **Bed API Endpoint:** https://sofasandstuff.com/Category/ProductPrice

---

## 💬 Communication Style

When working on this project:
- Keep technical explanations clear and detailed
- Use examples to illustrate concepts
- Reference specific line numbers when discussing code
- Update this context file with decisions made
- Document any "gotchas" or edge cases discovered

---

**End of Context File**

*This file should be updated at the end of each session to maintain continuity.*
