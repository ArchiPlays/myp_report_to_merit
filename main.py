import PyPDF2
import re
import tkinter as tk
from tkinter import filedialog, messagebox

subject_codes = {
    'Math': 'MA',
    'Sciences': 'SC',
    'Swedish': 'SW',
    'Acquisition': 'MS',
    'Individuals': 'IS',
    'Design': 'DS',
    'English': 'EN',
    'Physical': 'PH',
    'Ual Arts': 'AR',
    'Music': 'MU',
    'Acquisition: English': 'EL'
}

subject_codes_reverse = {
    'MA': 'Mathematics',
    'SC': 'Sciences',
    'SW': 'Swedish',
    'MS': 'Modern language',
    'IS': 'Individuals & Societies',
    'DS': 'Design',
    'EN': 'English Lang. Lit',
    'EL': 'English Lang. Acq',
    'PH': 'Physical & Health Ed',
    'AR': 'Visual Arts',
    'MU': 'Music'
}

    
subject_keywords = ['Math', 'Language', 'Individuals', 'Sciences', 'Arts', 'Physical', 'Design']
disregard = ['Service', 'Activities', '-']
lines = []
fg = {}

def set_lines(file_path):
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()

        if re.search(r'Summary of Achievement', page_text):
            global lines
            lines = page_text.split('\n')
            break

    pdf_file.close()
    
def read_subject_grades():
    for line in lines:
        for keyword in subject_keywords:
            if keyword in line and not any(dis in line for dis in disregard):
                for i in range(lines.index(line), len(lines)):
                    if re.search(r'\d{2}', lines[i]):
                        global fg
                        fg[code_from_line(line)] = lines[i][-1]
                        break
                break
    
def write_final_grades(file_path):
    with open(file_path, 'w') as file:
        for key, value in fg.items():
            file.write(f'{key}: {value}\n')

def grade_to_merit(key, grade):
    if grade >= 4:
        if key == 'EN':
            if grade == 7:
                return 20
            return 2.5 * grade + 5
        return 2.5 * grade + 2.5
    else:
        return 0
    
def code_from_line(line):
    for key in subject_codes.keys():
        if key.upper() in line.upper():
            if key == 'Literature':
                if 'Swedish' in line:
                    return 'SW'
                else:
                    return 'EN'
            return subject_codes[key]
    return None
            
def calculate_merit_points(swe):
    merit = 0
    subject_kw_weights = {
        'AR': 2,
        'DS': 2,
        'PH': 1,
        'SC': 3,
        'MA': 1,
        'MS': 1,
        'EN': 1,
        'IS': 4,
        'MU': 1,
        'EL': 1
    }
    
    # loop through fg and calculate merit points
    for key, value in fg.items():
        if key == 'SW':
            continue
        merit += subject_kw_weights[key] * grade_to_merit(key, int(value))
        
    if swe == 'A':
        merit += 20
    elif swe == 'B':
        merit += 17.5
    elif swe == 'C':
        merit += 15
    elif swe == 'D':
        merit += 12.5
    elif swe == 'E':
        merit += 10
    
    return merit

def calculate_merit_from_file(file_path, swe):
    set_lines(file_path)
    read_subject_grades()
    return calculate_merit_points(swe)
    
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        set_display_text('Merit points: ' + str(calculate_merit_from_file(file_path=file_path, swe=swe_var.get())))
        
        for key, value in fg.items():
            tk.Label(swe_frame, text=f'{subject_codes_reverse[key]}: {value}', padx=5, pady=1).pack()
        root.update()
        messagebox.showinfo("Success", "Grades processed and merit points calculated.")
    else:
        messagebox.showwarning("Warning", "No file selected.")

def set_display_text(text):
    display.config(text=text)
        
root = tk.Tk()
root.title("Merit Points Calculator")
root.geometry("300x600")

# create frame
frame = tk.Frame(root)
frame.pack(pady=20)

# create label
label = tk.Label(frame, text="Select your grades file:")
label.pack()

# create button
button = tk.Button(frame, text="Open file", command=open_file)
button.pack()

# create display
display = tk.Label(root, text="")
display.pack()

# create radio buttons
swe_var = tk.StringVar()
swe_var.set('A')
swe_frame = tk.Frame(root, pady=20)
swe_frame.pack()

swe_label = tk.Label(swe_frame, text="Swedish grade:")
swe_label.pack()

swe_a = tk.Radiobutton(swe_frame, text="A", variable=swe_var, value='A')
swe_a.pack()
swe_b = tk.Radiobutton(swe_frame, text="B", variable=swe_var, value='B')
swe_b.pack()
swe_c = tk.Radiobutton(swe_frame, text="C", variable=swe_var, value='C')
swe_c.pack()
swe_d = tk.Radiobutton(swe_frame, text="D", variable=swe_var, value='D')
swe_d.pack()
swe_e = tk.Radiobutton(swe_frame, text="E", variable=swe_var, value='E')
swe_e.pack()
swe_f = tk.Radiobutton(swe_frame, text="F", variable=swe_var, value='F')
swe_f.pack()

swe_label_2 = tk.Label(swe_frame, text="Only Sv & SvA valid, otw F", pady=5)
swe_label_2.pack()

grades_below = tk.Label(swe_frame, text="Grades are listed below.", pady=10)
grades_below.pack()

root.mainloop()
