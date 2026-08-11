import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import fitz
import threading
from collections import Counter
import re

# ---------------- GLOBAL ----------------
pdf_text = ""
dark_mode = False

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()

root.title("Smart PDF AI Assistant PRO")

root.geometry("1200x750")

root.configure(bg="#E6E6FA")

# ---------------- COLORS ----------------
BG = "#E6E6FA"
BTN = "purple"
FG = "white"

# ---------------- FUNCTIONS ----------------

# OPEN PDF
def open_pdf():

    global pdf_text

    file = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )

    if file:

        progress.start()

        pdf_name = file.split("/")[-1]

        pdf_label.config(
            text=f"Uploaded PDF: {pdf_name}"
        )

        try:

            doc = fitz.open(file)

            text_list = []

            for page in doc:

                text_list.append(
                    page.get_text()
                )

            pdf_text = "\n".join(text_list)

            output_box.delete(
                "1.0",
                tk.END
            )

            output_box.insert(
                tk.END,
                "✅ PDF Loaded Successfully!\n\n"
            )

            output_box.insert(
                tk.END,
                pdf_text
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        progress.stop()

# SUMMARY WITH WORD LIMIT
def summarize_pdf():

    if not pdf_text:

        messagebox.showwarning(
            "No PDF",
            "Please upload a PDF first."
        )

        return

    limit_window = tk.Toplevel(root)

    limit_window.title(
        "Summary Limit"
    )

    limit_window.geometry(
        "300x150"
    )

    tk.Label(
        limit_window,
        text="Enter summary word limit:",
        font=("Arial", 11)
    ).pack(pady=10)

    word_limit_entry = tk.Entry(
        limit_window,
        font=("Arial", 11)
    )

    word_limit_entry.pack(
        pady=5
    )

    word_limit_entry.insert(
        0,
        "100"
    )

    def generate_summary():

        try:

            limit = int(
                word_limit_entry.get()
            )

        except:

            messagebox.showerror(
                "Invalid",
                "Enter valid number"
            )

            return

        limit_window.destroy()

        def run():

            output_box.delete(
                "1.0",
                tk.END
            )

            output_box.insert(
                tk.END,
                "⏳ Generating Summary...\n\n"
            )

            words = pdf_text.split()

            summary = " ".join(
                words[:limit]
            )

            output_box.delete(
                "1.0",
                tk.END
            )

            output_box.insert(
                tk.END,
                f"📌 SUMMARY ({limit} words)\n\n"
            )

            output_box.insert(
                tk.END,
                summary
            )

        threading.Thread(
            target=run
        ).start()

    tk.Button(
        limit_window,
        text="Generate",
        command=generate_summary,
        bg="purple",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=10)

# QUESTION ANSWER
def ask_question():

    if not pdf_text:

        messagebox.showwarning(
            "No PDF",
            "Please upload a PDF first."
        )

        return

    question = question_entry.get().lower()

    if (
        question == ""
        or question == "ask anything from pdf..."
    ):
        return

    sentences = pdf_text.split(".")

    answer = "No answer found."

    question_words = [
        w for w in question.split()
        if len(w) > 2
    ]

    best_score = 0

    for sentence in sentences:

        score = sum(
            1
            for word in question_words
            if word in sentence.lower()
        )

        if score > best_score:

            best_score = score

            answer = sentence

    output_box.delete(
        "1.0",
        tk.END
    )

    output_box.insert(
        tk.END,
        "💡 ANSWER\n\n"
    )

    output_box.insert(
        tk.END,
        answer
    )

# GENERATE QUESTIONS
def generate_questions():

    if not pdf_text:

        messagebox.showwarning(
            "No PDF",
            "Please upload a PDF first."
        )

        return

    output_box.delete(
        "1.0",
        tk.END
    )

    output_box.insert(
        tk.END,
        "🧠 IMPORTANT QUESTIONS\n\n"
    )

    sentences = [
        s.strip()
        for s in pdf_text.split(".")
        if len(s.strip()) > 40
    ]

    for s in sentences[:5]:

        output_box.insert(
            tk.END,
            "• Explain: " + s + "?\n\n"
        )

# KEYWORD HIGHLIGHT
def highlight_keywords():

    if not pdf_text:

        messagebox.showwarning(
            "No PDF",
            "Please upload a PDF first."
        )

        return

    output_box.delete(
        "1.0",
        tk.END
    )

    words = re.findall(
        r'\b[a-zA-Z]{4,}\b',
        pdf_text.lower()
    )

    stop_words = {
        "this", "that", "with",
        "from", "have", "there",
        "their"
    }

    filtered = [
        w for w in words
        if w not in stop_words
    ]

    count = Counter(filtered)

    top = count.most_common(10)

    output_box.insert(
        tk.END,
        "🔑 TOP KEYWORDS\n\n"
    )

    for word, num in top:

        output_box.insert(
            tk.END,
            f"{word} → {num} times\n"
        )

# SEARCH
def search_word():

    word = search_entry.get()

    output_box.tag_remove(
        "search",
        "1.0",
        tk.END
    )

    start = "1.0"

    while True:

        pos = output_box.search(
            word,
            start,
            stopindex=tk.END,
            nocase=True
        )

        if not pos:
            break

        end = f"{pos}+{len(word)}c"

        output_box.tag_add(
            "search",
            pos,
            end
        )

        output_box.tag_config(
            "search",
            background="yellow"
        )

        start = end

# SAVE OUTPUT
def save_output():

    content = output_box.get(
        "1.0",
        tk.END
    )

    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file:

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        messagebox.showinfo(
            "Saved",
            "Output Saved!"
        )

# DARK MODE
def toggle_mode():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        root.configure(
            bg="#1E1E1E"
        )

        title.config(
            bg="#1E1E1E",
            fg="white"
        )

        greeting.config(
            bg="#1E1E1E",
            fg="white"
        )

        pdf_label.config(
            bg="#1E1E1E",
            fg="white"
        )

        output_box.config(
            bg="#252526",
            fg="white"
        )

    else:

        root.configure(
            bg="#E6E6FA"
        )

        title.config(
            bg="#E6E6FA",
            fg="purple"
        )

        greeting.config(
            bg="#E6E6FA",
            fg="black"
        )

        pdf_label.config(
            bg="#E6E6FA",
            fg="black"
        )

        output_box.config(
            bg="white",
            fg="black"
        )

# ---------------- TITLE ----------------
title = tk.Label(
    root,
    text="SMART PDF AI ASSISTANT",
    font=("Arial", 22, "bold"),
    bg=BG,
    fg="purple"
)

title.pack(
    pady=10
)

# ---------------- GREETING ----------------
greeting = tk.Label(
    root,
    text="Upload a PDF to begin smart analysis",
    font=("Arial", 11),
    bg=BG
)

greeting.pack()

# ---------------- PDF LABEL ----------------
pdf_label = tk.Label(
    root,
    text="No PDF Uploaded",
    font=("Arial", 12, "bold"),
    bg=BG
)

pdf_label.pack(
    pady=5
)

# ---------------- PROGRESS BAR ----------------
progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=300,
    mode="indeterminate"
)

progress.pack(
    pady=5
)

# ---------------- NOTEBOOK ----------------
notebook = ttk.Notebook(root)

notebook.pack(
    fill="both",
    expand=True
)

main_tab = tk.Frame(
    notebook,
    bg=BG
)

notebook.add(
    main_tab,
    text="Main"
)

# ---------------- BUTTONS ----------------
button_frame = tk.Frame(
    main_tab,
    bg=BG
)

button_frame.pack(
    pady=10
)

style = {
    "font": ("Arial", 10, "bold"),
    "bg": BTN,
    "fg": FG,
    "width": 18,
    "height": 2,
    "cursor": "hand2"
}

tk.Button(
    button_frame,
    text="Open PDF",
    command=open_pdf,
    **style
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

tk.Button(
    button_frame,
    text="Summarize",
    command=summarize_pdf,
    **style
).grid(
    row=0,
    column=1,
    padx=5
)

tk.Button(
    button_frame,
    text="Generate Questions",
    command=generate_questions,
    **style
).grid(
    row=0,
    column=2,
    padx=5
)

tk.Button(
    button_frame,
    text="Highlight Keywords",
    command=highlight_keywords,
    **style
).grid(
    row=0,
    column=3,
    padx=5
)

tk.Button(
    button_frame,
    text="Save Output",
    command=save_output,
    **style
).grid(
    row=0,
    column=4,
    padx=5
)

tk.Button(
    button_frame,
    text="Dark Mode",
    command=toggle_mode,
    **style
).grid(
    row=0,
    column=5,
    padx=5
)

# ---------------- QUESTION FRAME ----------------
question_frame = tk.Frame(
    main_tab,
    bg=BG
)

question_frame.pack(
    pady=15
)

question_entry = tk.Entry(
    question_frame,
    width=75,
    font=("Arial", 12),
    fg="gray"
)

question_entry.grid(
    row=0,
    column=0,
    padx=5,
    ipady=6
)

question_entry.insert(
    0,
    "Ask anything from PDF..."
)

# PLACEHOLDER FUNCTIONS
def clear_placeholder(event):

    if question_entry.get() == "Ask anything from PDF...":

        question_entry.delete(
            0,
            tk.END
        )

        question_entry.config(
            fg="black"
        )

def add_placeholder(event):

    if question_entry.get() == "":

        question_entry.insert(
            0,
            "Ask anything from PDF..."
        )

        question_entry.config(
            fg="gray"
        )

question_entry.bind(
    "<FocusIn>",
    clear_placeholder
)

question_entry.bind(
    "<FocusOut>",
    add_placeholder
)

# SEND BUTTON
send_button = tk.Button(
    question_frame,
    text="➤",
    command=ask_question,
    font=("Arial", 14, "bold"),
    bg="#19C37D",
    fg="white",
    width=3,
    height=1,
    bd=0,
    cursor="hand2",
    activebackground="#16a56b",
    activeforeground="white"
)

send_button.grid(
    row=0,
    column=1,
    padx=5
)

question_entry.bind(
    "<Return>",
    lambda event: ask_question()
)

# ---------------- SEARCH ----------------
search_frame = tk.Frame(
    main_tab,
    bg=BG
)

search_frame.pack(
    pady=10
)

search_entry = tk.Entry(
    search_frame,
    width=40,
    font=("Arial", 11)
)

search_entry.grid(
    row=0,
    column=0,
    padx=5
)

tk.Button(
    search_frame,
    text="Search Word",
    command=search_word,
    **style
).grid(
    row=0,
    column=1
)

# ---------------- OUTPUT BOX ----------------
output_box = scrolledtext.ScrolledText(
    main_tab,
    width=130,
    height=25,
    font=("Arial", 11)
)

output_box.pack(
    pady=10
)

# ---------------- RUN ----------------
root.mainloop() 