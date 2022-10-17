#define a function to generate Algorand wallet accounts, and search them for strings
#useful for creating a vanity algorand address
#you can search anywhere in the address, the front or the back of the address
#inspired by https://algovanity.com/

#run first, must be run
#import the relevant packages from AlgoSDK
from algosdk import account, mnemonic


def generate_algorand_keypair_search(searchterm, num, pos):
    private_key, address = account.generate_account()
    if pos == "A":
        if searchterm in address:
            print("My address: \n{}".format(address))
            print("My passphrase: \n{}".format(mnemonic.from_private_key(private_key)))
    elif pos == "F":
        if address[0:num] == searchterm:
            print("My address: \n{}".format(address))
            print("My passphrase: \n{}".format(mnemonic.from_private_key(private_key)))
    elif pos == "B":
        if address[-num:] == searchterm:
            print("My address: \n{}".format(address))
            print("My passphrase: \n{}".format(mnemonic.from_private_key(private_key)))
    else: 
        print("Pick F, A or B!")
        
        
#request number of keypairs to generate
y = int(input("Please enter the number of Algorand keypairs to generate: \n"))

#request (num)ber of digits, the searchterm, and whether to search
#at the (f)ront of the address, (b)ack of the address or (a)nywhere in the address
num = int(input("How many digits to search within the address: \n"))
searchterm = str(input(f"Type {num} character(s): \n"))
pos = str.upper(input("Do you want to search the (F)ront, (B)ack or (A)nywhere in the address: \n"))

#generate y keypairs, running them through the search function
#only displaying the addresses which match the search term
for i in range(y):
    generate_algorand_keypair_search(searchterm, num, pos)        
