destination = int(input())
input_list = input().split(' ')

done = False
distance_sum = 0

for i, jump in enumerate(input_list):
    jump = int(jump)
    if jump > 10:
        distance_sum = 0
        continue
    
    distance_sum += jump

    if distance_sum >= destination:
        done = True
        finish_idx = i + 1
        break

if done:
    print(f'done: {finish_idx}')
else:
    print(f'fail: {destination - distance_sum}')
