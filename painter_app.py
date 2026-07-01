import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io
import urllib.parse

def create_app():
    root = tk.Tk()
    root.title("AI Painter")
    root.geometry("700x800")

    def generate_image():
        prompt = prompt_entry.get()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt.")
            return

        status_label.config(text="Generating image...")
        root.update()

        try:
            # Encode the prompt for the URL
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

            response = requests.get(url, timeout=30)
            response.raise_for_status()

            image_data = response.content
            image = Image.open(io.BytesIO(image_data))

            # Resize image if it's too large for the window
            max_size = (600, 600)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            photo = ImageTk.PhotoImage(image)

            image_label.config(image=photo)
            image_label.image = photo # Keep a reference!

            status_label.config(text="Image generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate image: {e}")
            status_label.config(text="")

    tk.Label(root, text="Enter your idea:").pack(pady=10)

    prompt_entry = tk.Entry(root, width=50, font=("Arial", 14))
    prompt_entry.pack(pady=10)

    generate_btn = tk.Button(root, text="Draw it!", command=generate_image, font=("Arial", 12))
    generate_btn.pack(pady=10)

    status_label = tk.Label(root, text="", fg="blue")
    status_label.pack(pady=5)

    image_label = tk.Label(root)
    image_label.pack(pady=10)

    return root

if __name__ == "__main__":
    app = create_app()
    app.mainloop()
