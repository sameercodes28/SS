Step-by-Step Guide: Upgrading to Full-Scale App

You have successfully built the simple prototype. Now, let's upgrade it to handle all products on the S&S website.

This plan involves:

Running the Scraper to generate the 4 data files (the "brain").

Uploading a new main.py (which reads from these files) to your Google Cloud Function, overwriting the simple prototype.

Phase 1: Generate the Full "Brain" (Locally)

Save New Files:

In your sofa-price-tool folder, save the new files from our chat, overwriting your old main.py and requirements.txt files:

main.py (the new full-scale one)

requirements.txt (the new one with fuzzywuzzy)

sku_discovery_tool.py (the new scraper)

requirements_scraper.txt (the new scraper dependencies)

Install All Dependencies:

In your terminal (with the (venv) activated), install the libraries for both scripts:

pip install -r requirements_scraper.txt
pip install -r requirements.txt 


Run the Scraper:

This is the big step. Run the full scraper. This will take 30-60 minutes.

Use the full path to the venv Python executable to avoid ModuleNotFoundError:

./venv/bin/python sku_discovery_tool.py


The script will print its progress (e.g., [INFO] Fetching sofas..., [SUCCESS] Found SKU: 'alw'...). It is intentionally slow to avoid being blocked.

When it's done, you will have 4 new JSON files in your folder:

products.json

sizes.json

covers.json

fabrics.json

Phase 2: Test Full Backend Locally

Start Local Test Server:

Use the full path to the venv executable for functions-framework as well:

./venv/bin/functions-framework --target=http_entry_point --debug


Test with curl (in a new Terminal):

Now you can test any product, not just the hardcoded ones!

Test Chair: curl -X POST http://localhost:8080/getPrice -H "Content-Type: application/json" -d '{"query": "snape chair pacific"}'

Test Footstool: curl -X POST http://localhost:8080/getPrice -H "Content-Type: application/json" -d '{"query": "porthallow footstool waves"}'

Test Dog Bed: curl -X POST http://localhost:8080/getPrice -H "Content-Type: application/json" -d '{"query": "dog bed large biscuit"}'

Test Ambiguity: curl -X POST http://localhost:8080/getPrice -H "Content-Type: application/json" -d '{"query": "alwinton blue"}' (Should return an error with fabric suggestions).

Phase 3: Deploy the Full Backend

Deploy to Google Cloud:

This command will overwrite your old prototype function with the new, powerful version. It uploads main.py, requirements.txt, and all 4 new JSON files.

Make sure you are in your sofa-price-tool folder with your (venv) active.

gcloud functions deploy sofa-prototype-api \
  --gen2 \
  --runtime=python310 \
  --region=us-central1 \
  --source=. \
  --entry-point=http_entry_point \
  --trigger-http \
  --allow-unauthenticated


Note: If this fails, you may need to create a file named .gcloudignore and add venv/ to it, so it doesn't try to upload your virtual environment.

Phase 4: Final Test (Live)

Test Your Live App:

You don't need to change your frontend! Your index.html on GitHub Pages (https://sameercodes28.github.io/S-S/) will automatically call the new, smarter backend.

Go to your live github.io URL.

You can now query any product, size, and fabric on the entire website.

Test Queries:

"Snape chair pacific"

"Porthallow footstool waves"

"Dog bed large biscuit"

"Alwinton 3 seater loose cover waves" (tests the cover logic)

That's it! You've successfully upgraded your prototype to the full application.