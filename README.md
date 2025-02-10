# DipMCQPaper

DipMCQPaper is a Python project for scanning and grading multiple-choice question (MCQ) papers using OpenCV and QR code detection.

## Project Structure

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Pyzbar
- Pandas
- Tkinter

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/DipMCQPaper.git
    cd DipMCQPaper
    ```

2. Install the required packages:
    ```sh
    pip install opencv-python-headless numpy pyzbar pandas
    ```

## Usage

1. Run the main script:
    ```sh
    python OMR_Main.py
    ```

2. Follow the prompts to enter the number of questions and choices.

3. The script will capture images from the specified IP camera or use the provided image (`7.jpg`) for processing.

4. The results will be saved in [Marks.xlsx](http://_vscodecontentref_/3) and displayed in a popup message.

## Functions

### [utlis.py](http://_vscodecontentref_/4)

- [stackImages(imgArray, scale, lables=[])](http://_vscodecontentref_/5): Stacks multiple images for display.
- [reorder(myPoints)](http://_vscodecontentref_/6): Reorders corner points for perspective transformation.
- [rectContour(contours)](http://_vscodecontentref_/7): Finds rectangular contours.
- [getCornerPoints(cont)](http://_vscodecontentref_/8): Gets corner points of a contour.
- [splitBoxes(img, questions, choices)](http://_vscodecontentref_/9): Splits the image into boxes for each question and choice.
- [drawGrid(img, questions=5, choices=5)](http://_vscodecontentref_/10): Draws a grid on the image.
- [showAnswers(img, myIndex, grading, ans, questions=5, choices=5)](http://_vscodecontentref_/11): Shows the answers on the image.
- [get_qr_code_data(image)](http://_vscodecontentref_/12): Decodes QR code data from the image.
- [get_number_of_choices()](http://_vscodecontentref_/13): Prompts the user to enter the number of choices per question.
- [get_number_of_questions()](http://_vscodecontentref_/14): Prompts the user to enter the number of questions.
- [get_answers(number_of_questions, number_of_choices)](http://_vscodecontentref_/15): Prompts the user to enter the answers for each question.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
