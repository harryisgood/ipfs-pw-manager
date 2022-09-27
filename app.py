from flask import Flask, request, render_template
import sys
import requests
import json
import geocoder
from countrygroups import EUROPEAN_UNION
import subprocess
import secrets
import string

app = Flask(__name__)
DATA='earthquake_data1.txt'
out_DATA='new.txt'

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    # define the alphabet
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    alphabet = letters + digits + special_chars

    # fix password length
    pwd_length = 12

    # generate a password string
    pwd = ''
    for i in range(pwd_length):
        pwd += ''.join(secrets.choice(alphabet))

    print(pwd)

    # generate password meeting constraints
    while True:
        pwd = ''
        for i in range(pwd_length):
            pwd += ''.join(secrets.choice(alphabet))

        if (any(char in special_chars for char in pwd) and sum(char in digits for char in pwd)>=2):
            break
    return(pwd)

@app.route('/search_pw', methods=['POST', 'GET'])
def search_pw():
    password = ''
    if request.method == 'POST':
        name = request.form.get("name")
        
        f=open('hash.txt', 'r')
        hash=f.readlines()
        hash=hash[0] 
        output = subprocess.check_output(['ipfs', 'cat', hash])
        output = output.decode('utf-8')
        outputs = output.split('\n')
        stored = dict()
        outputs = outputs[:-1]
        for output in outputs:
            line = output.split(': ')
            stored[line[0]] = line[1]
              
        print('output', output, file=sys.stderr)
        
        #f= open('map.txt', 'r')
        #f.write(output)
        #f.close()
        password = stored[name] #output
    return render_template('index.html', password=password)

@app.route('/add_pw', methods=['POST', 'GET'])
def add_pw():
    print(request.method, file=sys.stderr)
    if request.method == 'POST':
        name = request.form.get("account_name")
        pw = generate()  #request.form.get('pw')
        
        new_ = str(name) + ': ' + str(pw) +'\n'
        f= open('map.txt', 'a')
        f.write(new_)
        f.close()

        output = subprocess.check_output(["ipfs", "add", "map.txt"])
        output = output.decode('utf-8')
        print(output, file=sys.stderr)
        output = output.split(' ')[1]
        print(output, file=sys.stderr)
        f=open('hash.txt', 'w')
        f.write(output)
        f.close()
        return render_template('index.html')

@app.route('/')
def index():
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port='5000')
