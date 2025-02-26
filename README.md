📝 GRADIENT – Automated MCQ Grading with OpenCV
DipMCQPaper is a Python-powered solution for scanning and grading multiple-choice question (MCQ) papers using OpenCV and QR code detection. Designed for accuracy and efficiency, this tool automates MCQ evaluations with real-time scanning and result generation.

🚀 Features
✔️ Automated Grading – Scan and evaluate MCQ papers instantly
✔️ QR Code Integration – Detect and decode unique paper identifiers
✔️ Intelligent Image Processing – Recognizes answer bubbles with high accuracy
✔️ Customizable Inputs – Define the number of questions and choices
✔️ Exportable Results – Saves grades to Marks.xlsx for easy access

📂 Project Structure
📁 DipMCQPaper
 ┣ 📜 OMR_Main.py        # Main script for scanning & grading
 ┣ 📜 utils.py           # Image processing helper functions
 ┣ 📜 requirements.txt   # Dependencies list
 ┣ 📜 README.md          # Project documentation
 ┣ 📁 data               # Sample MCQ papers & test images

🛠 Tech Stack
🔹 Python 3.x | OpenCV | NumPy | Pyzbar | Pandas | Tkinter

🔧 Installation & Setup
Clone the repository:
git clone https://github.com/yourusername/DipMCQPaper.git
cd DipMCQPaper

Install dependencies:
pip install -r requirements.txt

▶️ Usage
Run the grading script:
python OMR_Main.py

📌 Steps:
1️⃣ Enter the number of questions and choices
2️⃣ Capture or upload an MCQ paper image
3️⃣ View results in Marks.xlsx and a popup display

⚡ Core Functions
🔹 utlis.py (Image Processing):
✔ stackImages() – Combines multiple images for better visualization
✔ reorder() – Reorders corner points for accurate perspective transformation
✔ rectContour() – Identifies rectangular contours
✔ splitBoxes() – Extracts individual MCQ bubbles from the scanned image
✔ showAnswers() – Highlights correct and incorrect responses

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

🎯 Contributing
Contributions are welcome! Feel free to fork, improve, and submit a PR.

🚀 Let's automate MCQ grading like never before! 🖥️✨
