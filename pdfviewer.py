import fitz  # PyMuPDF module
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Viewer")
        self.pdf_doc = None
        self.current_page = 0

        # Canvas to display PDF
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Buttons
        self.btn_prev = tk.Button(root, text="Previous", command=self.prev_page)
        self.btn_prev.pack(side=tk.LEFT)

        self.btn_next = tk.Button(root, text="Next", command=self.next_page)
        self.btn_next.pack(side=tk.RIGHT)

        self.btn_open = tk.Button(root, text="Open PDF", command=self.load_pdf)
        self.btn_open.pack(side=tk.BOTTOM)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_doc = fitz.open(file_path)
            self.current_page = 0
            self.display_page()

    def display_page(self):
        if self.pdf_doc:
            pix = self.pdf_doc[self.current_page].get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.resize((800, 600))  # Resize for display
            self.img_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

    def next_page(self):
        if self.pdf_doc and self.current_page < len(self.pdf_doc) - 1:
            self.current_page += 1
            self.display_page()

    def prev_page(self):
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1
            self.display_page()

# Run GUI
root = tk.Tk()
app = PDFViewer(root)
root.mainloop()
