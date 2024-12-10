#define a function to generate Algorand wallet accounts, and search them for strings
#useful for creating a vanity algorand address
#you can search anywhere in the address, the front or the back of the address
#inspired by https://algovanity.com/
#note: the larger the search space, the more addresses that need to be generated to search
#searching for terms 5 letters long or longer will require at least millions of addresses to be generated

#import the relevant packages from AlgoSDK
from algosdk import account, mnemonic

#define non-multi search function
def generate_algorand_keypair_search(searchterm, num, pos):
    private_key, address = account.generate_account()
    if pos == "A":
        if searchterm in address:
            print("My address: \n{}".format(address))
            print("My passphrase: \n{}".format(mnemonic.from_private_key(private_key)))
    elif pos == "F":
        if address[:num] == searchterm:
            print("My address: \n{}".format(address))
            print("My passphrase: \n{}".format(mnemonic.from_private_key(private_key)))
    elif pos == "B":
        if address[-num:] == searchterm:
            print("My address: \n{}".format(address))
            print("My passphrase: \n{}".format(mnemonic.from_private_key(private_key)))
    else: 
        print("Pick F, A or B!")

#functions for multi-search        
def generate_algorand_keypair():
    private_key, address = account.generate_account()
    return private_key, address

def search_front(fterm, fnum, address):
    if address[0:fnum] == fterm:
        return address

def search_back(bterm, bnum, faddress):
    if faddress[-bnum:] == bterm:
        print("My address: \n{}".format(faddress))
        print("My passphrase: \n{}".format(mnemonic.from_private_key(private_key)))
        
        
#request number of keypairs to generate
y = int(input("Please enter the number of Algorand keypairs to generate: \n"))

#request multi_search setup
m = str.upper(input("Do you want to search the front + back? (Y)es or (N)o \n"))
if m == "Y":
    multi = True
else:
    multi = False
    
#multi-search allows user to search for keywords at both the front and the back of the address
if multi == True:
    #request parameters
    fnum = int(input("How many digits to search within the front of the address: \n"))
    fterm = str(input(f"Type {fnum} character(s): \n"))
    bnum = int(input("How many digits to search within the back of the address: \n"))
    bterm = str(input(f"Type {bnum} character(s): \n"))
    for i in range(y):
        private_key, address = generate_algorand_keypair()
        faddress = search_front(fterm, fnum, address)
        if faddress != None:
            search_back(bterm, bnum, faddress) 
            
#normal search function to search the (F)ront, (B)ack or (A)nywhere within an Algorand address            
else:
    #request parameters
    num = int(input("How many digits to search within the address: \n"))
    searchterm = str(input(f"Type {num} character(s): \n"))
    pos = str.upper(input("Do you want to search the (F)ront, (B)ack or (A)nywhere in the address: \n"))
    for i in range(y):
        generate_algorand_keypair_search(searchterm, num, pos)            
