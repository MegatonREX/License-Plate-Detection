import cv2
import imutils as imu
import pytesseract
import tkinter as tk
from tkinter import filedialog

pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"   

root=tk.Tk()

root.geometry("1000x500")
root.title("NSP Project")    

def returnpath():
    global file
    file = tk.filedialog.askopenfile(title="choose a file")

label=tk.Label(root,text='License Plate Detection',font=('Arial',32,'bold'), background='yellow')
label.pack()

bg=tk.PhotoImage(file="Poornima_University.png")    
                                                 
label=tk.Label(root, image=bg)
label.pack()

button=tk.Button(root,text='Copy',font=('Arial',10))
button.configure(bg="red", fg="white")
button.place(x=665,y=256)

entry=tk.Entry(root,width=50)
entry.pack()

button=tk.Button(root,text='Browse',font=('Arial',12),command=returnpath)
button.configure(width=5)
button.pack()

def main():
    img=cv2.imread(str(file.name))
    img=imu.resize(img, width=500)

    cv2.imshow('original image', img)  
    cv2.waitKey(0)

    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    cv2.imshow('gray image',gray)
    cv2.waitKey(0)

    gray=cv2.bilateralFilter(gray, 11,17,17)
    cv2.imshow('bilateral image', gray)
    cv2.waitKey(0)

    outlined=cv2.Canny(gray, 170,200)
    cv2.imshow('canny image',outlined)
    cv2.waitKey(0)

    cnts, new=cv2.findContours(outlined.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1=img.copy()
    cv2.drawContours(img1, cnts,  -1,(0,255,0),3)
    cv2.imshow('canny after contouring',img1)
    cv2.waitKey(0)

    cnts=sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCount=None
    img2=img.copy()
    cv2.drawContours(img2, cnts, -1, (0, 255, 0),3)

    count=0
    name=1

    for i in cnts:
        perimeter=cv2.arcLength(i, True)
        approx=cv2.approxPolyDP(i, 0.02*perimeter, True)

        if(len(approx)==4):
            NumberPlateCount=approx
            x, y, w, h=cv2.boundingRect(i)
            crp_img= img[y:y+h, x:x+w]

            cv2.imwrite(str(name)+ '.png', crp_img)
            name += 1

            break

    cv2.drawContours(img, NumberPlateCount, -1, (0,255,0), 3)
    cv2.imshow("final image",img)   
    cv2.waitKey(0)

    crp_img_loc='1.png'

    text=str(pytesseract.image_to_string(crp_img_loc, lang='eng'))
    print(str(text))
    entry.insert(tk.END,text)
    entry.pack()
    root.clipboard_append(text)
    root.update()


root.bind('<Return>',main)
button=tk.Button(root,text='Submit',font=('Arial',14,'bold'),command=main)
button.configure(bg='green')
button.pack(padx=10,pady=20)

root.mainloop()

