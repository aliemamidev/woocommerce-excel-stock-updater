# 🛒 WooCommerce Excel Stock Updater

A powerful Python tool to **bulk update stock quantities** of WooCommerce products using an **Excel file** (by Product ID or SKU).  
Perfect for store managers and developers who want to sync their inventory from Excel without manually editing products.

---

## 📌 Features

✅ Update product stock based on Excel data  
✅ Supports both **Product ID** and **SKU**  
✅ Fully configurable through `config.json`  
✅ Parallel API requests for high performance  
✅ Excel output with updated quantities  
✅ Logging of all operations and errors  

---

## 🧑‍💻 Author

**Seyed Ali Emami**  
📧 aliemamidev@gmail.com  
💼 [LinkedIn](https://www.linkedin.com/in/aliemdev/) – [GitHub](https://github.com/aliemamidev)

---

## 📁 Project Structure

```

woocommerce-excel-stock-updater/
├── main.py              ← Main script
├── config.json          ← All configurations (API, columns, filenames, etc.)
├── requirements.txt     ← Python dependencies
├── README.md            ← You're reading it
└── .gitignore           ← Optional Git ignore file

````

---

## ⚙️ Configuration

Edit the `config.json` file before running the script:

```json
{
  "woocommerce_api": {
    "url": "https://your-store.com/wp-json/wc/v3/products",
    "consumer_key": "ck_your_consumer_key",
    "consumer_secret": "cs_your_consumer_secret"
  },
  "excel": {
    "input_file": "input.xlsx",
    "output_file": "output_updated.xlsx",
    "product_identifier_column": "Code",
    "update_column": "New Quantity",
    "use_sku": false
  },
  "settings": {
    "max_threads": 10,
    "log_file": "product_update.log"
  }
}
````

### 🔄 `use_sku` explanation:

| Value   | Meaning                     | Example                         |
| ------- | --------------------------- | ------------------------------- |
| `false` | Use Product ID (e.g. `101`) | API URL: `/products/101`        |
| `true`  | Use SKU (e.g. `ABC123`)     | API URL: `/products?sku=ABC123` |

---

## 📥 Excel Input Format

The input Excel file should look like this:

| Code (or SKU) | ... |
| ------------- | --- |
| 101           |     |
| 102           |     |

* Replace `Code` with your actual column name if needed (adjust in `config.json`)
* You can add other columns; they won’t be affected.

---

## 🧪 Output

A new Excel file (`output_updated.xlsx`) will be created with updated stock quantities in the column specified (e.g. `New Quantity`).

---

## 🚀 Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Edit your `config.json` with your API info and Excel file details

3. Run the script:

```bash
python main.py
```

4. Check:

   * ✅ Your updated Excel file
   * 📄 The log file: `product_update.log`

---

## 📦 Dependencies

Listed in `requirements.txt`:

```txt
pandas
requests
tqdm
openpyxl
```

---

## 🛠️ Notes

* Make sure your WooCommerce store has REST API access enabled
* API key must have **read** permissions at minimum
* For SKU-based lookup, each SKU should be **unique**

---

## 📃 License

This project is released under the MIT License.

---

Enjoy automated stock updates! 🚀

```
