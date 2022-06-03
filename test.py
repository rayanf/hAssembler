class a:
    def __init__(self):
        self.a = 5
    def __del__(self):
        pass
    def printt(self):
        print(self.a)

class b:
    def __init__(self,a):
        self.instructor = a
    def __del__(self):
        pass




t = a()

tt = b(a)
tt.instructor.printt()
