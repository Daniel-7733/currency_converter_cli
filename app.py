from currency import show_history, clear_history, pdf_converter, converter, save_data
from tkinter import Tk, Label, Button, Frame, Entry, Text
from typing import Tuple, List




def page_reset() -> None:
    """
    Clear previous content.

    Returns:
        None
    """

    for widget in content_frame.winfo_children():
        widget.destroy()  # Clear previous content


def load_page_one() -> None:
    """
    Load the first page displaying the conversion history.

    Returns:
        None
    """

    page_reset()

    history_list: List[str] = show_history()
    history_text: str = "\n".join(history_list) if history_list else "No conversion history found."

    text_widget: Text = Text(content_frame, height=15, width=50, bg='lightyellow', font=('Courier', 10))
    text_widget.insert('1.0', f"📜 Last Conversion History Entries:\n\n{history_text}")
    text_widget.config(state='disabled')  # make it read-only
    text_widget.pack(padx=10, pady=20)

    clear_button: Button = Button(content_frame, text="🗑 Clear History", bg='red', fg='white', command=clear_history)
    clear_button.pack(pady=5)

    pdf_button: Button = Button(content_frame, text="PDF", bg='red', fg='white', command=pdf_converter)
    pdf_button.pack(pady=5)


def load_page_two() -> None:
    """
    Load the second page for converting currencies.

    Returns:
        None
    """

    page_reset()

    input_frame: Frame = Frame(content_frame, bg='#03fce7')
    input_frame.pack(pady=10)

    Label(input_frame, text="Amount:", bg='#03fce7', font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=5, sticky='e')
    amount_entry: Entry = Entry(input_frame, font=('Arial', 11))
    amount_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(input_frame, text="Currency Symbol:", bg='#03fce7', font=('Arial', 12, 'bold')).grid(row=1, column=0, padx=10, pady=5, sticky='e')
    symbol_entry: Entry = Entry(input_frame, font=('Arial', 11))
    symbol_entry.grid(row=1, column=1, padx=10, pady=5)

    button_frame: Frame = Frame(content_frame, bg='#03fce7')
    button_frame.pack(pady=5)

    done_button: Button = Button(button_frame, text='Convert', bg="#08e966", fg='black', font=('Arial', 11, 'bold'), width=10, command=lambda: on_done_button_click())
    done_button.grid(row=0, column=0, padx=10, pady=5)

    save_button: Button = Button(button_frame, text='Save', bg="#08e966", fg='black', font=('Arial', 11, 'bold'), width=10, command=lambda: on_save_button_click())
    save_button.grid(row=0, column=1, padx=10, pady=5)

    result_label: Label = Label(content_frame, text="💱 Conversion result will appear here.", bg='lightyellow', fg='black', width=60, height=4, wraplength=400, font=('Courier', 10), justify='left', anchor='nw', bd=2, relief='sunken')
    result_label.pack(padx=10, pady=15)

    def on_done_button_click() -> None:
        """
        Handle the "Convert" button click event.

        Returns:
            None
        """

        amount: str = amount_entry.get()
        symbol: str = symbol_entry.get().upper()

        try:
            date, money, symbol, converted, usd = converter(amount, symbol)
            result_label.config(text=f"💸 {money} {symbol} = {converted} {usd} on {date}")
        except Exception as e:
            result_label.config(text=f"❌ Error: {str(e)}")

    def on_save_button_click() -> None:
        """
        Handle the "Save" button click event.

        Returns:
            None
        """

        amount: str = amount_entry.get()
        symbol: str = symbol_entry.get().upper()

        try:
            record: Tuple[str, float, str, float, str] = converter(amount, symbol)
            save_data([record])
            result_label.config(text="✅ Data saved successfully.")
        except Exception as e:
            result_label.config(text=f"❌ Error saving data: {str(e)}")


def create_menu_button(parent, text, command) -> Button:
    """
    Create a menu button in the sidebar.

    Args:
        parent (Frame): The parent frame where the button will be added.
        text (str): The text to display on the button.
        command (function): The function to call when the button is clicked.

    Returns:
        Button: The created menu button.
    """

    button_frame: Frame = Frame(parent, bg='#c3c3c3')
    button_frame.pack(fill='x', pady=5)

    blue_line: Frame = Frame(button_frame, bg='#158aff', width=5)
    blue_line.pack(side='left', fill='y')

    button: Button = Button(button_frame, text=text, bg='#c3c3c3', bd=0, anchor='w', command=command)
    button.pack(side='left', fill='x', expand=True)

    return button


if __name__ == '__main__':
    # App start
    window: Tk = Tk()
    window.geometry("600x500")
    window.title("Currency Converter")
    window.config(bg="#03fce7")

    # === Use grid for layout ===
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)  # content_frame can expand

    # Left sidebar (gray box)
    gray_rectangle: Frame = Frame(window, bg='#c3c3c3', width=100, height=400)
    gray_rectangle.grid(row=0, column=0, sticky="ns")
    gray_rectangle.grid_propagate(False)

    # Main content frame
    content_frame: Frame = Frame(window, bg="#03fce7")
    content_frame.grid(row=0, column=1, sticky="nsew")

    # Sidebar content
    label: Label = Label(gray_rectangle, text="Menu", bg='#c3c3c3', bd=0)
    label.pack(pady=40, fill='x')

    create_menu_button(gray_rectangle, "Show History", load_page_one)
    create_menu_button(gray_rectangle, "Currency", load_page_two)

    window.mainloop()
