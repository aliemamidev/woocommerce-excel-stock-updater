import pandas as pd
import requests
import logging
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# ===============================
# Load Configuration
# ===============================
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api_config = config['woocommerce_api']
excel_config = config['excel']
settings = config['settings']

# ===============================
# Setup Logging
# ===============================
logging.basicConfig(
    filename=settings.get('log_file', 'product_update.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ===============================
# Load Excel File
# ===============================
input_path = Path(excel_config['input_file'])
output_path = Path(excel_config['output_file'])

if not input_path.exists():
    raise FileNotFoundError(f"Input Excel file not found: {input_path}")

df = pd.read_excel(input_path)
id_col = excel_config['product_identifier_column']
update_col = excel_config['update_column']
use_sku = excel_config.get('use_sku', False)

if id_col not in df.columns:
    raise ValueError(f"Column '{id_col}' not found in input file.")

# ===============================
# WooCommerce API Request
# ===============================
def get_stock(identifier: str):
    try:
        if use_sku:
            url = f"{api_config['url']}?sku={identifier}"
        else:
            url = f"{api_config['url']}/{identifier}"
        response = requests.get(url, auth=(api_config['consumer_key'], api_config['consumer_secret']), timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            data = data[0] if data else {}
        stock = data.get('stock_quantity')
        return identifier, int(stock) if stock is not None else 0
    except Exception as e:
        logging.warning(f"{identifier} -> Error: {e}")
        return identifier, None

# ===============================
# Process All Products
# ===============================
identifiers = df[id_col].dropna().astype(str).tolist()
results = []

print("🔄 Fetching stock quantities from WooCommerce...")
with ThreadPoolExecutor(max_workers=settings.get('max_threads', 10)) as executor:
    futures = {executor.submit(get_stock, pid): pid for pid in identifiers}
    for future in tqdm(as_completed(futures), total=len(futures), desc="Checking"):
        results.append(future.result())

# ===============================
# Update DataFrame and Save
# ===============================
updated_count = 0
for pid, stock in results:
    if stock is not None:
        df.loc[df[id_col] == pid, update_col] = stock
        logging.info(f"{pid} -> Stock: {stock}")
        updated_count += 1

df.to_excel(output_path, index=False)
print(f"\n✅ Updated {updated_count} products.")
print(f"📁 Output saved to: {output_path.resolve()}")
print(f"📄 Log file: {settings['log_file']}")
