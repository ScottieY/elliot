import csv
import datetime

max_days = 7

events = [[False] * 24 * 60 * 60 for i in range(max_days)]
d_format = '%Y-%m-%d %H:%M:%S'
current_day = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)

second_per_day = 24 * 60 * 60
eight_am = 8 * 60 * 60
ten_pm = 22 * 60 * 60

def findIndex(time):
    d_time = datetime.datetime.strptime(time.strip(), d_format)
    seconds = int((d_time - current_day).total_seconds())
    day_index = int(seconds / second_per_day)
    seconds_oneday = int(seconds % second_per_day)
    return day_index,seconds_oneday

with open('./calendar.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        userid, begin, end = line
        b_d_idx , b_s_idx = findIndex(begin)
        e_d_idx , e_s_idx = findIndex(end)

        if b_d_idx > max_days - 1:
            continue
        if e_d_idx > max_days - 1:
            e_d_idx = max_days - 1
            e_s_idx = second_per_day - 1

        if b_d_idx == e_d_idx:
            for i in range(b_s_idx,e_s_idx + 1):
                events[b_d_idx][i] = True
        else:
            for i in range(b_s_idx, ten_pm):
                events[b_d_idx][i] = True
            for j in range(b_d_idx + 1, e_d_idx):
                for i in range(eight_am,ten_pm):
                    events[j][i] = True
            for i in range(eight_am, e_s_idx + 1):
                events[e_d_idx][i] = True

longest = (0,0,-1)

for d in range(len(events)):
    day = events[d]
    start = eight_am
    end = eight_am
    while end < ten_pm:
        if day[end]:
            start = end + 1
        else:
            if (end - start) > (longest[2] - longest[1]):
                longest = (d,start,end)
        end += 1
    if longest[1] == eight_am and longest [2] == ten_pm - 1:
        break

begin = current_day + datetime.timedelta(days=longest[0],seconds=longest[1])
end = current_day + datetime.timedelta(days=longest[0],seconds=longest[2])

print(begin,end)
