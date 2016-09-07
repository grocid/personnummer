import random
import calendar

year_range = range(68, 100) + range(00,15)
month_range = [3,4,5,6,7,8,9,10] #range(1,13)
total_population = 9920881
file_n = 'BE0101N1.csv'
ds = [0]+range(1,10)*2

def days(year, month): 
    day_range = [31,28+calendar.isleap(year)*1,31,30,31,30,31,31,30,31,30,31]
    return range(1,day_range[month-1]+1)

def fday_range(year): 
    return [31,28+calendar.isleap(year)*1,31,30,31,30,31,31,30,31,30,31]

def last_digit(number): # Luhn
	return (10-sum([ds[((1+(i+1)%2)*int(x))] 
            for i,x in enumerate(str(number))]))%10

def gen_num():
    control_range = range(0,10)
    year = str(random.choice(year_range)).zfill(2)
    month = str(random.choice(month_range)).zfill(2)
    day = str(random.choice(days(int(year),int(month)))).zfill(2)
    
    nn = (year+month+day+
        str(random.choice(control_range))+
        str(random.choice(control_range))+
        str(random.choice(control_range)))
    
    return nn+str(last_digit(nn))

def compute_optimal_range(file, size, upper_bound, lower_bound):
    f = open(file)
    
    for line in f.readlines():
        line = line.split(';')
        if line[0] == '"\xe5lder"':
            years = [int(year.strip('\n').strip('\r').strip('\"')) for year in line[1:]]
        if line[0] == '\"totalt \xe5lder\"':
            cards = [int(card.strip('\n').strip('\r').strip('\"')) for card in line[1:]]
    
    dd = {}
    for c,y in zip(cards, years):
        dd[y] = c
    output_range = []
    tot = 0
    
    while size > 0 and len(dd) > 0:
        d = max(dd, key=dd.get)
        output_range.append(str(d))
        if d >= lower_bound and d <= upper_bound:
            size -= 1
            tot += dd[d]
        del dd[d]
    return output_range, tot

def probability(n, m, s):
    ssum = 0
    for y in n:
        qq = fday_range(int(y))
        for mm in m:
            ssum += qq[mm]
    return 1.0*s/(ssum*1000)

print '[+] Reading {0}...'.format((file_n))
year_range, tot = compute_optimal_range(file_n, 20,3000,-1)
print '[+] Read different {0} years, estimated success probability {1} %'.format(
                len(year_range),probability(year_range,month_range,tot))
for i in range(0, 100): print gen_num()

