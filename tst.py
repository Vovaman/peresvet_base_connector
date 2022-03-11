
def ch(tag):
    tag["prsUse"] = "maybe"

tag1 = {"id": 1, "prsUse": "Yes"}
tag2 = {"id": 2, "prsUse": "No"}
ar1 = [tag1, tag2]
ar2 = [
    {
        "c": "t",
        "tag": tag1
    },
    {
        "c": "g",
        "tag": tag2
    }
]

#tag1["prsUse"] = "maybe"
ch(tag1)

print(f'ar1: {ar1[0]}\n')
print(f'ar2: {ar2[0]}\n')

'''
class A:
    def __init__(self):
        self.id = 10

    def wr(self):
        print(self.id)

class B(A):
    def wr(self):
        super().wr()
        print("B wr")

b = B()
b.wr()
'''
