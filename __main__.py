import tkinter as tk
from tkinter import messagebox
from web3 import Web3
from eth_account import Account
import secrets
import threading
import time

def generate_pair():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    _account = Account.from_key(private_key)
    return _account

def check_prefix(prefix_):
    _address = '0x' + prefix_ + '0' * (40 - len(prefix_))
    try:
        Web3.to_checksum_address(_address)
    except ValueError:
        return False
    else:
        return True

def check_suffix(suffix_):
    _address = '0x' + suffix_ + '0' * (40 - len(suffix_))
    try:
        Web3.to_checksum_address(_address)
    except ValueError:
        return False
    else:
        return True

def look_for_address(prefix, suffix, multiple):
    loop = 0
    global stop_search
    start_time = time.time()
    while not stop_search:
        loop += 1
        elapsed_time = time.time() - start_time
        progress_label.config(text=f"Generated: {loop} addresses | Time Elapsed: {elapsed_time:.2f} seconds")
        root.update_idletasks()
        account = generate_pair()
        address_prefix = account.address[2:2 + len(prefix)]
        address_suffix = account.address[42 - len(suffix):]
        if address_prefix == prefix and address_suffix == suffix:
            result_textbox.insert(tk.END, f"Generated {loop} addresses\nAddress: {account.address}\nPrivate Key: {account.key.hex()}\n\n")
            with open('wallets.txt', 'a') as fp:
                fp.write(f'{account.address},{account.key.hex()}\n')
            if not multiple:
                break

def on_generate():
    global stop_search
    if generate_button['text'] == "Generate Wallet":
        prefix = prefix_entry.get()
        suffix = suffix_entry.get()
        multiple = multiple_var.get()

        if len(prefix) == 0 and len(suffix) == 0:
            messagebox.showerror("Input Error", "Please provide a prefix or suffix.")
            return

        if len(prefix) > 0 and not check_prefix(prefix):
            messagebox.showerror("Input Error", "Incorrect prefix checksum.")
            return

        if len(suffix) > 0 and not check_suffix(suffix):
            messagebox.showerror("Input Error", "Incorrect suffix checksum.")
            return

        result_textbox.delete(1.0, tk.END)
        progress_label.config(text="Looking for address...")
        stop_search = False
        generate_button.config(text="Stop")
        threading.Thread(target=look_for_address, args=(prefix, suffix, multiple), daemon=True).start()
    else:
        stop_search = True
        generate_button.config(text="Generate Wallet")

def main():
    # GUI Setup
    global root, main_frame, prefix_entry, suffix_entry, multiple_var, generate_button, progress_label, result_textbox, stop_search
    root = tk.Tk()
    root.title("Vanity Ethereum Wallet Generator")
    root.geometry("500x550")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Frame Setup to Handle Resizing
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_rowconfigure(8, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    # Prefix Input
    tk.Label(main_frame, text="Prefix:").grid(row=0, column=0, pady=5, sticky='w')
    prefix_entry = tk.Entry(main_frame, width=50)
    prefix_entry.grid(row=1, column=0, pady=5, sticky='ew')

    # Suffix Input
    tk.Label(main_frame, text="Suffix:").grid(row=2, column=0, pady=5, sticky='w')
    suffix_entry = tk.Entry(main_frame, width=50)
    suffix_entry.grid(row=3, column=0, pady=5, sticky='ew')

    # Multiple Wallets Checkbox
    multiple_var = tk.BooleanVar()
    multiple_checkbox = tk.Checkbutton(main_frame, text="Generate Multiple Wallets", variable=multiple_var)
    multiple_checkbox.grid(row=4, column=0, pady=5, sticky='w')

    # Generate Button
    generate_button = tk.Button(main_frame, text="Generate Wallet", command=on_generate)
    generate_button.grid(row=5, column=0, pady=20, sticky='ew')

    # Progress Label
    progress_label = tk.Label(main_frame, text="")
    progress_label.grid(row=6, column=0, pady=5, sticky='w')

    # Result Textbox
    result_textbox = tk.Text(main_frame, height=10)
    result_textbox.grid(row=7, column=0, pady=10, sticky='nsew')

    # GitHub Link
    github_label = tk.Label(main_frame, text="Made by gensx-x1: https://github.com/gensx-x1", fg="blue", cursor="hand2")
    github_label.grid(row=8, column=0, pady=5, sticky='w')
    github_label.bind("<Button-1>", lambda e: root.clipboard_append("https://github.com/gensx-x1"))

    # Global Variable to Control Thread
    stop_search = False

    root.mainloop()

if __name__ == "__main__":
    main()
