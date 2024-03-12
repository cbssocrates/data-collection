import statistics
import numpy
with open("statistics.txt", "r") as file:
    t0, t1, t2, t3, v1, v2 = [], [], [], [], [], []
    for line in file.readlines():
        if eval(line.split()[-4]) >= 0.0:
            t0.append(eval(line.split()[-4]))
        if eval(line.split()[-3]) >= 0.0:
            t1.append(eval(line.split()[-3]))
        if eval(line.split()[-2]) >= 0.0:
            t2.append(eval(line.split()[-2]))
        if eval(line.split()[-1]) >= 0.0:
            t3.append(eval(line.split()[-1]))
        else:
            t3.append(eval(line.split()[-2]))

        v1.append(line.split()[0])
        v2.append(line.split()[1])

    t0, t1, t2, t3 = numpy.array(t0), numpy.array(
        t1), numpy.array(t2), numpy.array(t3)
    print(min(t0), min(t1), min(t2), min(t3))
    print(max(t0), max(t1), max(t2), max(t3))

    print(min(t1 - t0), statistics.mean(t1 - t0), statistics.median(t1-t0))
    print(min(t3 - t2), statistics.mean(t3 - t2), statistics.median(t3-t2))

    print(set(v1))
    print(set(v2))
