# BMI計算
"""
weight=float(input('体重(kg)を入力してください：'))
height=float(input('身長(m)を入力してください：'))
bmi = weight/(height*height)
print('結果：',bmi)
"""

# 簡単なリスト+

"""
names=['tom','james','jordan','ann']
print(names[0])#1番目の人
print(names[-2])#後ろから2番目の人
print(len(names))#人数
"""
"""
print(10>10) #False
print('ab' in 'abcd') #True
    
"""

# 条件分岐

# answer1の回答は１、answer2の回答は２
"""
answer1=int(input('解答１の点数は？'))
answer2=int(input('解答２の点数は？'))
if answer1==1 and answer2==5:
    print('両方正解')
else:
    if answer1==1:
        print('解答１だけが正解')
    elif answer2==5:
        print('解答２だけが正解')
    else:
        print('両方正解')
"""
# 繰り返し処理

# 1~100までの値の合計
"""
num=1
result=0
while num<101:
    result+=num
    num+=1
print('1～１００の合計は',result)
"""
"""
num=0
for i in range(1,101):
    num+=i
print('１～１００の合計は',num)
"""

# 文字列の操作
"""
phase='i want to eat apple and banana'
print(phase.split('banana'))
"""

# 関数
# 三角の面積
"""
def get_triangle(base=1,height=1):
    return base*height/2
print(get_triangle()) #1*1/2
area=get_triangle(5,4)
print(area) #4*5/2
"""
# 台形の面積
"""
def get_trapezoid(upper=10,lower=10,height=10):
    return (upper+lower)*height/2
print('台形の面積は',get_trapezoid(upper=2,height=3))
"""

# クラスにメソッドを追加する
"""
class Person:
    def __init__(self, name, height, weight):
        self.name = name
        self.height = height
        self.weight = weight
    
    def bmi(self):
        result = self.weight/(self.height*self.height)
        print(self.name, 'のBMIの値は', result, 'です。')

    def work(self):
        print(self.name, 'is working')

p1=Person('tom', 1.21, 23)
p1.bmi()
p1.work()
"""