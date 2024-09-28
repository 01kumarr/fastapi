def find_armstrong(num : int):
    chars = chr(num)
    n = len(chars) 

    _sum = 0
    while num > 0:
        r = num % 10 
        _sum = _sum + r**n 
        num = num//10 

    return num == _sum 

if find_armstrong(135):
    print("yes this is the armstrong number")
else:
    print("No this is not armstrong number") 

