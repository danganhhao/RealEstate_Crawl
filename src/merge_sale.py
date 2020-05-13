fout = open("realestate_data_sale_merge.csv", "a", encoding='utf-8')
for line in open("realestate_data_100.csv"):
    fout.write(line)

for num in range(2, 97):
    if num != 95:
        f = open("realestate_data_" + str(num) + "00.csv")
        f.__next__()
        for line in f:
            fout.write(line)
        f.close()
        print("Done - " + str(num))

f = open("realestate_data_9693.csv")
f.__next__()
for line in f:
    fout.write(line)
f.close()
print("Done - " + str(num))

fout.close()
