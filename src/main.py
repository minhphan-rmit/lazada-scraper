import tkinter as tk
from tkinter import filedialog
from scraper import ScrapeLazada  # Assuming ScrapeLazada is in a separate file named ScrapeLazada.py

class LazadaScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Lazada Scraper")

        # URL Label and Text Entry
        self.label_url = tk.Label(master, text="Initial URL")
        self.label_url.pack()

        self.entry_url = tk.Entry(master)
        self.entry_url.pack()

        # Total Pages Label and Text Entry
        self.label_pages = tk.Label(master, text="Total Pages")
        self.label_pages.pack()

        self.entry_pages = tk.Entry(master)
        self.entry_pages.pack()

        # Destination Folder Label and Button
        self.label_destination = tk.Label(master, text="Destination Folder")
        self.label_destination.pack()

        self.button_destination = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.button_destination.pack()

        # Start Button
        self.start_button = tk.Button(master, text="Start Scraping", command=self.start_scraping)
        self.start_button.pack()

        # Status Label
        self.status_label = tk.Label(master, text="", fg="green")
        self.status_label.pack()

        # Variables to store user inputs
        self.url = None
        self.total_pages = 0
        self.destination_folder = None

    def select_folder(self):
        self.destination_folder = filedialog.askdirectory()
        if self.destination_folder:
            self.status_label.config(text="Selected folder: " + self.destination_folder)

    def start_scraping(self):
        self.url = self.entry_url.get()
        try:
            self.total_pages = int(self.entry_pages.get())
        except ValueError:
            self.status_label.config(text="Please enter a valid number for total pages", fg="red")
            return

        if not self.url or self.total_pages <= 0 or not self.destination_folder:
            self.status_label.config(text="Please enter all fields correctly", fg="red")
            return

        self.status_label.config(text="Scraping started...", fg="green")
        
        # Start scraping in a separate thread if needed
        scraper = ScrapeLazada(self.url, self.total_pages, self.destination_folder)
        scraper.scrape()
        self.status_label.config(text="Scraping completed. Data saved in " + self.destination_folder, fg="green")

def main():
    root = tk.Tk()
    gui = LazadaScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
