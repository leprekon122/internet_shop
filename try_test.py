# def work(n):
#    for i in range(1, n+1):
#        if i % 3 == 0 and i % 5 == 0:
#            print('FizzBuzz')
#        elif i % 3 == 0 and i % 5 != 0:
#            print('Fizz')
#        elif i % 3 != 0 and i % 5 == 0:
#            print('Buzz')
#        else:
#            print(i)

# print(work(15))


class MyTest:
    def __init__(self, **kwargs):
        self.data = kwargs
        for key, value in self.data.items():
            if key != 'count':
                print(f'{key}: {value}')
        print(f"count: {self.data['count']}")

    def __len__(self):
        res = len(self.data)
        return res - 1


data = {'name': 'nick',
        'age': 22}

a = MyTest(count=3, name='R2D2', age=66, planet='Naboo')

print(a)
print(a.__len__())
