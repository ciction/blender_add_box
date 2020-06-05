# import numpy as np
# a = np.array([4,2,7])
# b = [n**2 for n in a]

# print(a)
# print(b)


# presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
# for num, name in enumerate(presidents, start=1):
#     print("President {}: {}".format(num, name))


# for x in range(0, 3):
#     print("We're on time %d" % (x))


print("----------------------")
# faces_template=[2,4,6,8]
# for x in range(0, len(faces_template)*5):
#     repeatingIndex = faces_template[ x % len(faces_template) ]
#     loopCounter =  x // len(faces_template)
#     print(repeatingIndex + loopCounter)


print("----------------------")
# faces_template=[2,4,6,8]
# for x in range(0, len(faces_template)*5):
#     repeatingIndex = faces_template[ x % len(faces_template) ]
#     loopCounter =  x // len(faces_template)
#     offset = loopCounter *  len(faces_template)
#     print(offset)


faces_template = [
    # bottom
    [0, 1, 2, 3],
    # top
    [4, 5, 6, 7],
    # back
    [0, 1, 5, 4],
    # front
    [2, 3, 7, 6],
    # left
    [0, 4, 7, 3],
    # right
    [6, 5, 1, 2]
]

faces = []
for x in range(0, len(faces_template)*2):
    repeatingIndex = faces_template[x % len(faces_template)]
    loopCounter = x // len(faces_template)
    offset = loopCounter * 8


    offset_vector = [offset,offset,offset,offset]
    newVector = [repeatingIndex[i]+offset_vector[i] for i in range(len(repeatingIndex))]
    faces.append(newVector)


print(faces)
