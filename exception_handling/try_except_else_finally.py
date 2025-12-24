# Python code to illustrate 
# working of try()  
def divide(x, y): 
    try: 
        # Floor Division : Gives only Fractional 
        # Part as Answer 
        result = x // y 
    except ZeroDivisionError: 
        print("Sorry ! You are dividing by zero ") 
    else:
        print("Yeah ! Your answer is :", result) 
    finally:  
        # this block is always executed   
        # regardless of exception generation.  
        print('This is always executed')
        print("="*50)   

# Look at parameters and note the working of Program 
divide(3, 2)
divide(3, 0)