import cv2
import numpy as np
from pyzbar.pyzbar import decode
from tkinter import simpledialog,messagebox
import tkinter as tk



def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) 
    print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) 
    add = myPoints.sum(1)
    print(add)
    print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)] 
    myPointsNew[3] =myPoints[np.argmax(add)]   
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  
    myPointsNew[2] = myPoints[np.argmax(diff)] 
    return myPointsNew

def rectContour(contours):

    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            #approx = cv2.approxPolyDP(curve, epsilon, closed)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) 
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) 
    return approx

def splitBoxes(img,questions,choices):
    rows = np.vsplit(img,questions)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,choices)
        for box in cols:
            boxes.append(box)
    return boxes

def drawGrid(img,questions=5,choices=5):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/choices)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)

    return img

def showAnswers(img,myIndex,grading,ans,questions=5,choices=5):
     secW = int(img.shape[1]/questions)
     secH = int(img.shape[0]/choices)

     for x in range(0,questions):
         myAns= myIndex[x]
         cX = (myAns * secW) + secW // 2
         cY = (x * secH) + secH // 2
         if grading[x]==1:
            myColor = (0,255,0)
            #cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
            cv2.circle(img,(cX,cY),50,myColor,cv2.FILLED)
         else:
            myColor = (0,0,255)
            #cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
            cv2.circle(img, (cX, cY), 50, myColor, cv2.FILLED)

            
            myColor = (0, 255, 0)
            correctAns = ans[x]
            cv2.circle(img,((correctAns * secW)+secW//2, (x * secH)+secH//2),
            20,myColor,cv2.FILLED)



def get_qr_code_data(image):
    decoded_objects = decode(image)
    qr_data = None
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 255, 0), 2)
    return qr_data





def get_number_of_choices():
    root = tk.Tk()
    root.withdraw() 
    while True:
        
        number_of_choices = simpledialog.askinteger("Input", "Enter the number of choices per question:", minvalue=2, maxvalue=10)
        
       
        if number_of_choices is None:
            messagebox.showwarning("Input Needed", "You must enter a valid number between 2 and 10. Defaulting to 4.")
            return 4  
        
        if 2 <= number_of_choices <= 10:
            root.destroy()  
            return number_of_choices
        else:
            
            messagebox.showerror("Invalid Input", "Please enter a number between 2 and 10.")

    root.destroy()  
def get_number_of_questions():
    root = tk.Tk()
    root.withdraw()
    while True:
        try:
            number_of_questions = simpledialog.askinteger("Input", "Enter the number of questions:", minvalue=1, maxvalue=100)
            
            if number_of_questions is None:
                messagebox.showerror("Invalid Input", "You must enter a valid number between 1 and 100.")
                continue

            if 1 <= number_of_questions <= 100:
                root.destroy()
                return number_of_questions
            else:
                messagebox.showerror("Invalid Input", "Please enter a number between 1 and 100.")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value.")
            
    root.destroy()

def get_answers(number_of_questions, number_of_choices):
    root = tk.Tk()
    root.withdraw()  

    answers = []
    
    
    valid_range = (1, 5)

    for i in range(1, number_of_questions + 1):
        while True:
            answer = simpledialog.askinteger(
                "Input", 
                f"Enter the answer for question {i} (1-{number_of_choices}):", 
                minvalue=1, 
                maxvalue=number_of_choices
            )

           
            if answer is None:
                messagebox.showwarning("Input Needed", "Invalid input detected. Defaulting to 1.")
                answers.append(1)  
                break

            
            if valid_range[0] <= answer <= valid_range[1]:
                answers.append(answer - 1)  
                break
            else:
               
                messagebox.showerror("Invalid Input", f"Please enter a number between {valid_range[0]} and {valid_range[1]}.")

    root.destroy() 
    return answers
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from tkinter import simpledialog,messagebox
import tkinter as tk



def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) 
    print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32) 
    add = myPoints.sum(1)
    print(add)
    print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)] 
    myPointsNew[3] =myPoints[np.argmax(add)]   
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  
    myPointsNew[2] = myPoints[np.argmax(diff)] 
    return myPointsNew

def rectContour(contours):

    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            #approx = cv2.approxPolyDP(curve, epsilon, closed)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) 
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) 
    return approx

def splitBoxes(img,questions,choices):
    rows = np.vsplit(img,questions)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,choices)
        for box in cols:
            boxes.append(box)
    return boxes

def drawGrid(img,questions=5,choices=5):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/choices)
    for i in range (0,9):
        pt1 = (0,secH*i)
        pt2 = (img.shape[1],secH*i)
        pt3 = (secW * i, 0)
        pt4 = (secW*i,img.shape[0])
        cv2.line(img, pt1, pt2, (255, 255, 0),2)
        cv2.line(img, pt3, pt4, (255, 255, 0),2)

    return img

def showAnswers(img,myIndex,grading,ans,questions=5,choices=5):
     secW = int(img.shape[1]/questions)
     secH = int(img.shape[0]/choices)

     for x in range(0,questions):
         myAns= myIndex[x]
         cX = (myAns * secW) + secW // 2
         cY = (x * secH) + secH // 2
         if grading[x]==1:
            myColor = (0,255,0)
            #cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
            cv2.circle(img,(cX,cY),50,myColor,cv2.FILLED)
         else:
            myColor = (0,0,255)
            #cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
            cv2.circle(img, (cX, cY), 50, myColor, cv2.FILLED)

            
            myColor = (0, 255, 0)
            correctAns = ans[x]
            cv2.circle(img,((correctAns * secW)+secW//2, (x * secH)+secH//2),
            20,myColor,cv2.FILLED)



def get_qr_code_data(image):
    decoded_objects = decode(image)
    qr_data = None
    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], True, (0, 255, 0), 2)
    return qr_data





def get_number_of_choices():
    root = tk.Tk()
    root.withdraw() 
    while True:
        
        number_of_choices = simpledialog.askinteger("Input", "Enter the number of choices per question:", minvalue=2, maxvalue=10)
        
       
        if number_of_choices is None:
            messagebox.showwarning("Input Needed", "You must enter a valid number between 2 and 10. Defaulting to 4.")
            return 4  
        
        if 2 <= number_of_choices <= 10:
            root.destroy()  
            return number_of_choices
        else:
            
            messagebox.showerror("Invalid Input", "Please enter a number between 2 and 10.")

    root.destroy()  
def get_number_of_questions():
    root = tk.Tk()
    root.withdraw()
    while True:
        try:
            number_of_questions = simpledialog.askinteger("Input", "Enter the number of questions:", minvalue=1, maxvalue=100)
            
            if number_of_questions is None:
                messagebox.showerror("Invalid Input", "You must enter a valid number between 1 and 100.")
                continue

            if 1 <= number_of_questions <= 100:
                root.destroy()
                return number_of_questions
            else:
                messagebox.showerror("Invalid Input", "Please enter a number between 1 and 100.")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric value.")
            
    root.destroy()

def get_answers(number_of_questions, number_of_choices):
    root = tk.Tk()
    root.withdraw()  

    answers = []
    
    
    valid_range = (1, 5)

    for i in range(1, number_of_questions + 1):
        while True:
            answer = simpledialog.askinteger(
                "Input", 
                f"Enter the answer for question {i} (1-{number_of_choices}):", 
                minvalue=1, 
                maxvalue=number_of_choices
            )

           
            if answer is None:
                messagebox.showwarning("Input Needed", "Invalid input detected. Defaulting to 1.")
                answers.append(1)  
                break

            
            if valid_range[0] <= answer <= valid_range[1]:
                answers.append(answer - 1)  
                break
            else:
               
                messagebox.showerror("Invalid Input", f"Please enter a number between {valid_range[0]} and {valid_range[1]}.")

    root.destroy() 
    return answers