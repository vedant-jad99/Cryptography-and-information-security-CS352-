#!/usr/bin/env python3

from math import sqrt
from tkinter import Frame, Button, Label, Entry, GROOVE, Tk
from datetime import datetime, date
from os.path import exists, dirname, realpath, join

class CryptFunctions:
    def __init__(self):
        #Object creation only. No functionality need here
        pass

    def extract_prime_factors(self, n):
        prime_factors = {}
        while n%2 == 0: 
            try:
                prime_factors[2] += 1
            except KeyError:
                prime_factors[2] = 1
            n = n//2

        for i in range(3, int(sqrt(n))+1,2): 
            while n%i == 0: 
                try:
                    prime_factors[i] += 1
                except KeyError:
                    prime_factors[i] = 1
                n = n//i 

        if n > 2:
            prime_factors[n] = 1
        return prime_factors 

    def gcd(self, a, b):
        if(a == 0):
            return b
        else:
            return self.gcd(b%a, a)

    # Main code segment
    def mobius_function(self, n):
        if n == 1:
            return 1
        count = 0
        prime_factors = self.extract_prime_factors(n)
        for value in prime_factors.values():
            if value > 1:
                return 0
            count += 1
        if count%2 == 0:
            return 1
        return -1
        
    def euler_totient_function(self, n):
        phi = 1
        for i in range(2, n):
            if self.gcd(i, n) == 1:
                phi += 1
        return phi

class UI:
    def __init__(self, root):
        self.log = None
        self.logfile_name = join(dirname(realpath(__file__)), "logfile.log")
        
        self.frame1 = Frame(root, padx=10, pady=5)
        self.frame2 = Frame(root, pady=10, padx=20)
        self.frame3 = Frame(root, pady=10, padx=20)
        self.answer = Button(self.frame2, text="ANSWER", relief=GROOVE, borderwidth=5, width=15, command=self.initiate)
        self.input_box = Entry(self.frame1)
        label = Label(self.frame1, text="Enter a number", width=15, padx=10)
        
        mobius_label = Label(self.frame2, text="Mobius function value", width=25, padx=10)
        euler_totient_label = Label(self.frame2, text="Euler's totient function value", width=25, padx=10)
        self.mobius = Entry(self.frame2, width=40)
        self.euler = Entry(self.frame2, width=40)
        self.warning = Label(self.frame3, fg="red")
        
        label.grid(row=0, column=0)
        mobius_label.grid(row=1, column=0, padx=10)
        euler_totient_label.grid(row=2, column=0, padx=10)
        self.input_box.grid(row=0, column=1)
        self.answer.grid(row=0, column=0, pady=10)
        self.mobius.grid(row=1, column=1, pady=10)
        self.euler.grid(row=2, column=1, pady=10)
        self.warning.grid(row=0, column=0, pady=5)
        self.frame1.grid(row=0, column=0, pady=10)
        self.frame2.grid(row=1, column=0, pady=10)
        self.frame3.grid(row=2, column=0, pady=10)

    def initiate(self):
        if exists(self.logfile_name):
            self.log = open(self.logfile_name, "a")
        else:
            self.log = open(self.logfile_name, "w")

        n = self.input_box.get()
        mobius_text = self.mobius.get()
        euler_text = self.euler.get()
        self.mobius.delete(0, len(mobius_text))
        self.euler.delete(0, len(euler_text))
        try:
            val = int(n)
            assert val > 0, "AssertionError: Value should be greater than 0"
            self.warning.config(text="")
            msg = str(date.today()) + " - " + str(datetime.now().strftime("%H:%M:%S")) + " [ERROR: None] --- Value input : " + n + "\n"
            self.calculate(val)
        except ValueError:
            self.input_box.delete(0, len(n))
            self.warning.config(text="ValueError: Input should be an integer")
            msg = str(date.today()) + " - " + str(datetime.now().strftime("%H:%M:%S")) + " [ERROR: ValueError] --- Value input : " + n + "\n"
        except AssertionError as e:
            self.input_box.delete(0, len(n))
            self.warning.config(text=e)
            msg = str(date.today()) + " - " + str(datetime.now().strftime("%H:%M:%S")) + " [ERROR: AssertionError] --- Value input : " + n + "\n"
        self.log.write(msg)

    def calculate(self, n):
        crypt_obj = CryptFunctions()
        self.mobius.insert(0, str(crypt_obj.mobius_function(n)))
        self.euler.insert(0, str(crypt_obj.euler_totient_function(n)))


if __name__ == '__main__':
    root = Tk()
    ui = UI(root)
    root.mainloop()
    