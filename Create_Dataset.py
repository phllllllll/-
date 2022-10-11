import random
import numpy as np
import os
class Create_data():

    def Get_information(self):
        firstName = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹窦章云苏潘葛范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐"
        firstName2 = "万俟司马上官欧阳夏侯诸葛东方皇甫尉迟理塘"
        girl = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'
        boy = '丁伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国真中凯歌易仁器义礼智信友胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'
        fir = []
        sec = []
        sex = []
        age = []
        grade = []
        for i in range(90):
            grade.append(random.uniform(2, 4))
            age.append(random.choice(range(20,23)))
        grade.sort()
        grade.reverse()
        for x in range(90):
            if random.randint(0, 100) < 5:
                i = random.choice(range(len(firstName2)-1))
                if i % 2 != 0:
                    i+=1
                fir.append(firstName2[i:i+2])
            else:
                fir.append(random.choice(firstName))
            sex2 = random.choice(range(2))
            t = random.randint(0, 100)
            if sex2 > 0:
                sex.append('男')
                if t < 70:
                    sec.append(random.choice(boy) + random.choice(boy))
                else:
                    sec.append(random.choice(boy))
            else:
                sex.append('女')
                if t < 70:
                    sec.append(random.choice(girl) + random.choice(girl))
                else:
                    sec.append(random.choice(girl))
        return fir,sec,sex,age,grade
    def Class_ad(self, p):  # 随机数生成函数
        Student_ad = []
        for i in range(0, 20):  # 初始化所有人都来了
            l_temp = []
            for j in range(0, 90):
                l_temp.append(1)
            Student_ad.append(l_temp)

        Count = random.randint(5, 8)
        a = []
        for i in range(0, 90):
            a.append(i)
        l_student = np.random.choice(a, Count, replace=False, p=p)
        for x in l_student:
            l_class = []
            while (len(l_class) < 16):
                y = random.randint(0, 19)
                if y not in l_class:
                    l_class.append(y)
                    Student_ad[y][x] = 0
        for i in range(0, 20):
            Count = random.randint(0, 3)
            while (Count > 0):
                x = random.randint(0, 89)
                if Student_ad[i][x] == 1:
                    Student_ad[i][x] = 0
                    Count = Count - 1
        return Student_ad
    def Create_class(self, p, number):
        dic = { 0:'五', 1:'一', 2:'二', 3:'三', 4:'四'}
        File_name = '.\课程'  + str(dic[number % 5]) + '.csv'
        if(number <= 25):
            File_name = '.\Train\Train_dataset' + str(number) + '.csv'
        Student_ad = self.Class_ad(p)
        with open(File_name, 'w') as m:
            msg1 = '编号' + ',' + '姓名' + ',' + '性别' + ',' + '年龄' + ',' + '绩点'
            for i in range(0, 20):
                msg1 = msg1 + ',' + '出勤' + str(i + 1)
            m.write('{}\n'.format(msg1))
            fir, sec, sex, age, grade = self.Get_information()
            for i in range(0, 90):
                msg = str(i + 1) + ',' + fir[i] + sec[i] + ',' + sex[i] + ',' + str(age[i]) + ',' + str(grade[i])
                for j in range(0, 20):
                    msg = msg + ',' + str(Student_ad[j][i])
                m.write('{}\n'.format(msg))
    def Create_p(self):
        sum = 1
        q = 3
        len = 15
        Count = (90 // len)
        for i in range(0, len):
            sum = sum * q
        k = 1 / sum * (q - 1)
        p = []
        t = []
        for i in range(0, len):
            if i < 1:
                t.append(k)
                for j in range(0, Count):
                    p.append(k / Count)
            else:
                x = p[Count * i - 1] * q
                for j in range(0, Count):
                    p.append(x)
        p_all = 0
        for i in range(0, 89):
            p_all = p_all + p[i]
        p[89] = 1 - p_all
        return p
def main():
    try:
        os.makedirs(r'.\Train')
    except:
        temp = 1
    p = Create_data().Create_p()
    for i in range(1, 31):
        Create_data().Create_class(p, i)
main()