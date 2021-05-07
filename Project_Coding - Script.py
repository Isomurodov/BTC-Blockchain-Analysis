import requests
import time
import matplotlib.pyplot as plt


                            # Retrieving the data from blockchain.info with API (I PART)  
answer = False

while(not answer):
    try:
        r = requests.get('https://blockchain.info/rawblock/000000000000000000049cf366ee312547cee0cde82e419f9b701c178ae399fb') #/rawblock/hash_of_the_block
        a = r.json()
        answer = True
    except (Exception):
        print('An error occured, retry later')
        time.sleep(1)
       

                            # Processing the data (II PART)               
def minmax(mini_maxi, d):
    check = True
    for i in d:
        for j in d[i]:
            if check:
                res = j
                check = False
            if mini_maxi == 'maxi':
                if j > res:
                    res = j
                    ad = i
            else:
                if j < res:
                    res = j
                    ad = i
                    
    return res, 'by address', ad

ins = 0
outs = 0
dic = {} #amount of money moved in each transaction
lst = [] #those transactions where the sender moved his/her money back to him/herself
check = []
adr = {} #to store adresses and how much money was left in each address upon processing the block
dic_ins = {}
dic_outs = {}
fees = [] #fees

for i in a['tx'][1:]:
    fees.append(i['fee'])
    for j in i['inputs']:
        ins += j['prev_out']['value']
        check.append(j['prev_out']['addr'])
        if j['prev_out']['addr'] in dic_ins:
            dic_ins[j['prev_out']['addr']] += [ins]
        else:
            dic_ins[j['prev_out']['addr']] = [ins]
        if j['prev_out']['addr'] in adr:
            adr[j['prev_out']['addr']] -= j['prev_out']['value']
    for k in i['out']:
        if 'addr' in k and 'addr' in  j['prev_out']:
            if k['addr'] not in check:
                outs += k['value']
            else:
                lst.append(a['tx'].index(i))
        if k['addr'] in adr:
            adr[k['addr']] += k['value']
        else:
            adr[k['addr']] = k['value']
        if k['addr'] in dic_outs:
            dic_outs[k['addr']] += [outs]
        else:
            dic_outs[k['addr']] = [outs]
    dic[a['tx'].index(i)] = outs
    outs = 0
    ins = 0
    check = []

print('average amount of money moved in the block is ', sum([dic[i] for i in dic])/len(dic), 'S') #average amount of money moved in the block

print('max fee paid is ' + str(max(fees)) + 'S;', 'min fee paid is ' + str(min(fees)) + 'S') #max & min fee

fee_ratio = {i:fees[i-1]/dic[i] for i in dic if dic[i] > 0} #ratio (percentage) of fees/transactions

print('max output is', minmax('maxi', dic_outs)) #max output
print('min output is', minmax('mini', dic_outs)) #min output
print('max input is', minmax('maxi', dic_ins)) #max input
print('min input is', minmax('mini', dic_ins)) #min input  

dic_sorted = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])} #dic sorted by value
cnt = 0
for i in dic_sorted:
    if cnt == 0:
        print('min amount of transaction was', dic_sorted[i], 'moved in transactions #', i) #min amount of money moved & order number of the transaction
    if cnt == len(dic) - 1:
        print('max amount of transaction was', dic_sorted[i], 'moved in transaction #', i) #max amount of money moved & order number of the transaction
    cnt += 1        


                           #GRAPHS  (III PART)    
small_tx = [dic[i] for i in dic if dic[i] <= 1000000]
medium_tx = [dic[i] for i in dic if 1000000 < dic[i] <= 100000000]
big_tx = [dic[i] for i in dic if dic[i] > 100000000]
xx = [dic[i] if i != 1374 else 0 for i in dic]

plt.figure(figsize=(5, 40))

plt.subplot(611)
plt.hist(small_tx, bins=100) 
plt.title('density plot (less than 1000000)')
plt.xlabel('amount of transaction')
plt.ylabel('number of transactions')

plt.subplot(612)
plt.hist(medium_tx, bins=100)
plt.title('density plot (between 1000000 and 100000000 S)')
plt.xlabel('amount of transaction')
plt.ylabel('number of transactions')

plt.subplot(613)
plt.hist(big_tx, bins=100) 
plt.title('density plot (bigger than 100000000)')
plt.xlabel('amount of transaction')
plt.ylabel('number of transactions')

plt.subplot(614)
plt.plot(range(1696), xx) #graphic visualization of transactions and their amount
plt.title('graphic visualization of transactions')
plt.xlabel('order of transaction')
plt.ylabel('amount of transaction in 10s of BTC')

plt.subplot(615)
plt.plot(range(len(fees)), fees) #graphic visualization of fees
plt.title('fees')
plt.xlabel('order of transaction')
plt.ylabel('amount of transaction')

plt.subplot(616)
plt.hist([fee_ratio[i] for i in fee_ratio if fee_ratio[i] < 0.01], bins = 100) #density plot of fee ratios
plt.title('Fees ratio')
plt.xlabel('Percentages')
plt.ylabel('order number of transaction')

plt.suptitle('GRAPHS')
plt.show()
