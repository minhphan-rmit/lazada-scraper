import tkinter as tk
from tkinter import filedialog
from scraper import ScrapeLazada

class LazadaScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Lazada Scraper")

        self.label1 = tk.Label(master, text="URL")
        self.label1.pack()

        self.url_entry = tk.Entry(master)
        self.url_entry.pack()

        self.label2 = tk.Label(master, text="Total Pages")
        self.label2.pack()

        self.pages_entry = tk.Entry(master)
        self.pages_entry.pack()

        self.label3 = tk.Label(master, text="Destination File Path")
        self.label3.pack()

        self.filepath_entry = tk.Entry(master)
        self.filepath_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.start_button = tk.Button(master, text="Start Scraping", command=self.start_scraping)
        self.start_button.pack()

    def browse_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        self.filepath_entry.delete(0, tk.END)
        self.filepath_entry.insert(0, file_path)

    def start_scraping(self):
        url = self.url_entry.get()
        total_pages = int(self.pages_entry.get())
        file_path = self.filepath_entry.get()

        scraper = ScrapeLazada(url, total_pages, file_path)
        scraper.scrape()

def main():
    root = tk.Tk()
    window_width = 400
    window_height = 300

    # Get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # Set the window size and position it at the center
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    gui = LazadaScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
