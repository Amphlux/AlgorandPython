from algosdk import account, mnemonic
from tqdm import tqdm

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

# Request number of keypairs to generate
y = int(input("Please enter the number of Algorand keypairs to generate: \n"))

# Request multi_search setup
m = str.upper(input("Do you want to search the front + back? (Y)es or (N)o \n"))
if m == "Y":
    multi = True
else:
    multi = False

# Multi-search allows user to search for keywords at both the front and the back of the address
if multi == True:
    # Request parameters
    fnum = int(input("How many digits to search within the front of the address: \n"))
    fterm = str(input(f"Type {fnum} character(s): \n"))
    bnum = int(input("How many digits to search within the back of the address: \n"))
    bterm = str(input(f"Type {bnum} character(s): \n"))
    
    print("\nSearching for addresses... Press Ctrl+C to stop")
    for i in tqdm(range(y), desc="Generating addresses", unit="addr"):
        private_key, address = generate_algorand_keypair()
        faddress = search_front(fterm, fnum, address)
        if faddress != None:
            search_back(bterm, bnum, faddress)

else:
    # Request parameters
    num = int(input("How many digits to search within the address: \n"))
    searchterm = str(input(f"Type {num} character(s): \n"))
    pos = str.upper(input("Do you want to search the (F)ront, (B)ack or (A)nywhere in the address: \n"))
    
    print("\nSearching for addresses... Press Ctrl+C to stop")
    for i in tqdm(range(y), desc="Generating addresses", unit="addr"):
        generate_algorand_keypair_search(searchterm, num, pos)
