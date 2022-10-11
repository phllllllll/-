import torch
import csv
import numpy as np
from Create_Dataset import Create_data
w = torch.zeros((90, 1), dtype=torch.float32)
b = torch.zeros(1, dtype=torch.float32)
w.requires_grad_(requires_grad=True)
b.requires_grad_(requires_grad=True)
def net(x, w, b):
    return torch.mm(x, w) + b
def loss(y_hat, y):
    return (y_hat - y.view(y_hat.size())) ** 2 / 2
def sgd(params, lr):
    for param in params:
        param.data -= lr * param.grad
def Test(All_class_vec, Clicked_num):
    index = []
    for i in range(0, 90):
        index.append(i)
    dic = sorted((dict(zip(sum(w.detach().numpy().tolist(), []), index))).items(), key=lambda x: x[0], reverse=True)
    All_success_clicked = 0
    All_clicked = 0
    for i in range(0, 5):
        Class_vec = All_class_vec[i]
        Success_clicked = []
        Fail_click = []
        No_Rcall_Student = []
        for j in range(0, 90):
            Success_clicked.append(0)
            Fail_click.append(0)
        for j in range(0, 20):
            temp = 0
            for key, Student_ID in dic:
                temp = temp + 1
                if temp >= Clicked_num:
                    break
                if Student_ID in No_Rcall_Student:
                    continue
                if Class_vec[j][Student_ID] == 1:
                    All_success_clicked = All_success_clicked + 1
                    All_clicked = All_clicked + 1
                    Success_clicked[Student_ID] = Success_clicked[Student_ID] + 1
                    if Success_clicked[Student_ID] > 16:
                        Fail_click.append(Student_ID)
                else:
                    Fail_click[Student_ID] = Fail_click[Student_ID] + 1
                    All_clicked = All_clicked + 1
                    if Fail_click[Student_ID] > 4:
                        No_Rcall_Student.append(Student_ID)
    return All_success_clicked / All_clicked
def Train(Train_data):
    y_all = []
    for j in range(0, 20):
        temp = 0
        for Student_ID in range(0, 90):
            if Train_data[j][Student_ID] == 1:
                temp = temp + 1
        y_all.append(temp)
    for j in range(0, 20):
        x = Train_data[j].reshape((1, 90))
        y = torch.tensor([y_all[j]])
        Loss = loss(net(x, w, b), y).sum()
        Loss.backward()
        sgd([w, b], 0.0001)
        w.grad.data.zero_()
        b.grad.data.zero_()
def Create_student_ad(file_name):
    File = csv.reader(open(file_name))
    index = -1
    Student_ad = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for row in File:
        if index == -1:
            index = index + 1
            continue
        for j in range(5, 25):
            Student_ad[j - 5].append(float(1 - int(row[j])))
    Student_ad = torch.Tensor(Student_ad)
    return Student_ad
def main():
    Clicked_num = 6
    for i in range(0, 25):
        file_name ='.\Train\Train_dataset' + str(i + 1) + '.csv'
        Train(Create_student_ad(file_name))
    dic = {0:'五', 1:'一', 2:'二', 3:'三', 4:'四'}
    All_class_vec = []
    for i in range(0, 5):
        file_name = '.\课程' + dic[i] + '.csv'
        All_class_vec.append(Create_student_ad(file_name))
    print(Test(All_class_vec, Clicked_num))
main()