


#with open('./input/Subtlex.US.txt') as f:
with open('./input/FAN.txt') as f:
    for i, line in enumerate(f):
#        with open("../ambigClass-subtl/wiki/l{}.txt".format(str(i+1)), "w") as txtfile:
        with open("../ambigClass-FAN/wiki/{}.txt".format(str(i+1)),"w") as txtfile:
            txtfile.write(line)
        if i % 100 == 0:
            print(i)
