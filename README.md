# 💱 Currency Converter CLI with GUI

This is a simple Currency Converter app built with **Python** and **Tkinter** that allows you to:

- Convert foreign currencies to USD using live exchange rates
- Save your conversions to a CSV file
- View recent conversion history
- Export history as a PDF
- Use both a Command-Line Interface (CLI) and a Graphical User Interface (GUI)

---

## 📦 Features

- ✅ Real-time exchange rate fetching
- ✅ Simple and clean GUI using `tkinter`
- ✅ CSV data storage
- ✅ PDF export of history
- ✅ Clear and readable interface
- ✅ Error handling for invalid inputs

---

## 📁 Project Structure

```plaintext
currency_converter_cli/
│
├── app.py               # Main GUI application
├── currency.py          # Logic and conversion functionality
├── currency_data.csv    # Auto-generated file to store saved conversions
├── currency.json        # Currency symbol information (optional)
├── .gitignore           # Git ignored files
└── __pycache__/         # Python cache (auto-generated)
