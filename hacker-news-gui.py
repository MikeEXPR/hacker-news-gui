import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Function to fetch Hacker News headlines
def fetch_headlines():
    try:
        result_label.config(text="Fetching headlines...")
        root.update()  # Update the GUI while fetching data
        
        # Fetch top story IDs
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        if response.status_code != 200:
            raise Exception("Failed to fetch story IDs.")
        
        story_ids = response.json()[:10]  # Get top 10 story IDs
        headlines = []

        # Fetch details for each story ID
        for story_id in story_ids:
            url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            story_response = requests.get(url)
            if story_response.status_code == 200:
                story_data = story_response.json()
                headlines.append(story_data.get("title", "No Title"))

        # Update the result label with headlines
        result_text.set("\n".join(f"{i+1}. {headline}" for i, headline in enumerate(headlines)))
        result_label.config(text="Fetched headlines successfully!")

    except Exception as e:
        result_label.config(text="Error fetching headlines.")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Initialize GUI
root = tk.Tk()
root.title("Hacker News GUI Scraper")
root.geometry("600x400")

# Styling
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#0078D7")

# Header
header_label = ttk.Label(root, text="Hacker News Top Headlines", font=("Arial", 14, "bold"))
header_label.pack(pady=10)

# Fetch Button
fetch_button = ttk.Button(root, text="Fetch Headlines", command=fetch_headlines)
fetch_button.pack(pady=10)

# Result Box
result_text = tk.StringVar()
result_box = tk.Label(root, textvariable=result_text, font=("Arial", 12), justify="left", anchor="nw")
result_box.pack(padx=20, pady=10, fill="both", expand=True)

# Status Label
result_label = ttk.Label(root, text="", font=("Arial", 10))
result_label.pack(pady=10)

# Run GUI
root.mainloop()