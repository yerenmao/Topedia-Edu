num = int(input())

name = []
height = []
weight = []

for i in range(num):
    info_list = input().split(',')
    name.append(info_list[0])
    height.append(int(info_list[1]))
    weight.append(int(info_list[2]))

height_mean = round(sum(height) / num, 2)
weight_mean = round(sum(weight) / num, 2)

print(name)
print(height)
print(weight)
print(height_mean, weight_mean, sep=',')
