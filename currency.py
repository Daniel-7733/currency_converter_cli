from typing import Dict, List, Tuple
from requests import get, Response
from tkinter import filedialog
from datetime import datetime
from fpdf import FPDF
import csv
import os




CSV_PATH: str = 'currency_data.csv'
API_URL: str = 'https://moneymorph.dev/api/latest'



def request_rates() -> Dict[str, float]:
    """
    Fetches the latest currency exchange rates from an external API.

    Returns:
        Dict[str, float]: A dictionary mapping currency symbols to their exchange rates.
                          Returns an empty dictionary if the request fails.
    """

    try:
        response: Response = get(API_URL)
        response.raise_for_status()
        data = response.json()
        return {symbol: rate for symbol, rate in data['rates'].items()}
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return {}

def save_data(records: List[Tuple[str, float, str, float, str]], filename: str = CSV_PATH) -> None:
    """
    Saves currency conversion records to a CSV file.

    Args:
        records (List[Tuple[str, float, str, float, str]]): A list of conversion records,
            each containing date, amount, currency, converted amount, and USD symbol.
        filename (str, optional): The path to the CSV file. Defaults to CSV_PATH.

    Returns:
        None
    """

    headers = ['Date', 'Amount', 'Currency', 'Amount in USD', 'USD']
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(headers)
        writer.writerows(records)
    print(f"✅ Data saved to {filename}")


def show_history(filename: str = CSV_PATH) -> List[str]:
    """
    Retrieves and formats the last 10 entries from the currency conversion history.

    Args:
        filename (str, optional): The path to the CSV file containing history. Defaults to CSV_PATH.

    Returns:
        List[str]: A list of formatted strings representing the last 10 conversion entries.
    """

    history_list: List[str] = []

    if not os.path.exists(filename):
        print("No conversion history found.")
        return []

    with open(filename, 'r') as file:
        next(file)  # skip header
        for line in file:
            date, amount, currency, result, usd = line.strip().split(',')
            history_list.append(f"{date} | {amount}{currency} is {result}{usd}")


    # Get the last 5 entries (or fewer if less than 10)
    last_five_items: List[str] = history_list[-10:]

    return last_five_items


def clear_history() -> None:
    """
    Clears all currency conversion history by overwriting the CSV file with headers only.

    Returns:
        None
    """

    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w') as file:
            file.write("date,amount,currency,result,usd\n")  # just write header
    # load_page_one()  # Refresh


def pdf_converter() -> None:
    """
    Generates a PDF file containing the latest currency conversion history.

    Prompts the user to choose a save location using a file dialog.

    Returns:
        None
    """

    history_info: List[str] = show_history()  # Assuming show_history() returns a list of strings
    pdf: FPDF = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt="Search History", ln=1, align='C')
    
    # Join the history list into a single string
    history_text: str = "\n".join(history_info)
    pdf.multi_cell(0, 10, txt=history_text)  # Using multi_cell for multi-line text

    # ask the user where it wants to save the file
    file_path: str = filedialog.asksaveasfilename(
        defaultextension=".pdf",  # Default extension
        filetypes=[("PDF files", "*.pdf")],  # Only show PDF files
        title="Save PDF As"  # Dialog title
    )
    
    if file_path:  # If the user selected a location
        pdf.output(file_path)  # Save the PDF to the chosen location
        print(f"File saved as: {file_path}")
    else:
        print("Save operation cancelled.")


def check_amount(value: str) -> float:
    """
    Validates and converts a value to a float representing a monetary amount.

    Args:
        value (str): The input value to convert.

    Returns:
        float: The numeric representation of the value.
               Returns a string message if conversion fails.
    """

    while True:
        try:
            return float(value)
        except ValueError:
            return "Add number"


def check_symbol(user_input: str, valid_symbols: List[str]) -> str:
    """
    Validates if the provided currency symbol is among the valid options.

    Args:
        user_input (str): The currency symbol input by the user.
        valid_symbols (List[str]): A list of valid currency symbols.

    Returns:
        str: The valid symbol if found, otherwise an error message string.
    """

    while True:
        if user_input in valid_symbols:
            return user_input
        return "❌ Invalid currency symbol."


def converter(get_amount: str, get_symbol: str) -> Tuple[str, float, str, float, str]:
    """
    Converts an amount from a selected currency to USD using live exchange rates.

    Args:
        get_amount (str): The amount to be converted as a string input.
        get_symbol (str): The currency symbol to convert from.

    Returns:
        Tuple[str, float, str, float, str]: A tuple containing:
            - Date of conversion
            - Original amount
            - Original currency symbol
            - Converted amount in USD
            - USD symbol

    Raises:
        ValueError: If the currency symbol is not found in the exchange rate data.
    """

    rates: Dict[str, float]= request_rates()
    symbol_list: List[str]= list(rates.keys())

    money: float = check_amount(get_amount)
    symbol: str = check_symbol(get_symbol, symbol_list)
    rate: float = rates.get(symbol)
    date: str = datetime.now().strftime("%d/%m/%Y")
    
    if rate:
        converted = round(money / rate, 2)
        print(f"💱 {money} {symbol} = {converted} USD")
        return date, money, symbol, converted, '$'
    else:
        raise ValueError("Currency not found in rate data.")
    