from algosdk import account, mnemonic
from tqdm import tqdm
import json
import os

def display_logo():
    """Display ASCII art of the Algorand logo at startup."""
    logo = """
*   
*                       /\\
*                      /  \\ 
*                     /    \\
*                    /      \\
*                   /        \\
*                  /          \\
*                 /   //\\      \\
*                /   //  \\      \/     //
*               /   //    \\      \    //
*              /   //      \\      \\  //
*             /   //        \\      \\//
*            /   //         /\\      \\
*           /   //         /  \\      \\
*          /   //         /    \\      \\
*         /   //         /    //\\      \\
*        /   //         /    //  \\      \\
*       /   //         /    //    \\      \\
*      /   //         /    //      \\      \\
*     /   //         /    //        \\      \\
*    
*          ╔═╗╦  ╔═╗╔═╗╦═╗╔═╗╔╗╔╔╦╗
*          ╠═╣║  ║ ╗║ ║╠╦╝╠═╣║║║ ║║
*          ╩ ╩╩═╝╚═╝╚═╝╩╚═╩ ╩╝╚╝═╩╝
*         Vanity Address Generator
*                ----------
* Generate an algorand vanity address.
* CharSet: ABCDEFGHIJKLMNOPQRSTUVWXYZ234567
* Last character *must* end with the following: I, Y, Q, U, A, 4, M, E
* Length: 58
* FRONT example: EXAMPLE(the rest of the wallet)
* BACK example: (the rest of the wallet)EXAMPLE
* ANYWHERE example: EXAMPLE can appear anywhere in the key
* FRONT/BACK example: EXAM(the rest of the key)PLE
* BACK Last Char excluded example: (the rest of wallet)EXAMPLE# (# = valid random end char)
    """
    print(logo)

ALGORAND_ADDRESS_LENGTH = 58
VALID_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
VALID_END_CHARS = {'I', 'Y', 'Q', 'U', 'A', '4', 'M', 'E'}

def load_search_terms_file():
    """Load search terms from a JSON file."""
    while True:
        filename = input("\nEnter the path to your search terms file (or press Enter to skip): ").strip()
        
        if not filename:  # User pressed Enter without entering a filename
            return None
            
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found.")
            continue
            
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            if "search_terms" not in data:
                print("Error: File must contain a 'search_terms' array.")
                continue
                
            terms = []
            nums = []
            positions = []
            exclude_lasts = []
            
            for term_data in data["search_terms"]:
                if term_data["position"] == "FB":
                    # Handle Front & Back combination
                    terms.extend([f"F&B:{term_data['front_term']}", term_data['back_term']])
                    nums.extend([term_data['front_digits'], term_data['back_digits']])
                    positions.extend(["F", "B"])
                    exclude_lasts.extend([False, term_data['exclude_last']])
                else:
                    # Handle single position terms
                    terms.append(term_data["term"])
                    nums.append(term_data["digits"])
                    positions.append(term_data["position"])
                    exclude_lasts.append(term_data.get("exclude_last", False))
            
            # Validate the loaded terms
            for i, (term, num, pos) in enumerate(zip(terms, nums, positions)):
                if not validate_search_term(term):
                    print(f"Error: Invalid characters in term '{term}'")
                    return None
                    
                if len(term) != num:
                    print(f"Error: Term '{term}' length doesn't match specified digits {num}")
                    return None
                    
                if pos == "B" and not exclude_lasts[i]:
                    valid, message = validate_end_chars(term)
                    if not valid:
                        print(f"Error in term '{term}': {message}")
                        return None
            
            return terms, nums, positions, exclude_lasts
            
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in file.")
        except KeyError as e:
            print(f"Error: Missing required field {e} in search terms file.")
        except Exception as e:
            print(f"Error loading file: {str(e)}")
        
        retry = input("Would you like to try another file? (Y/N): ").upper()
        if retry != "Y":
            return None


def validate_search_term(term):
    """Check if search term contains only valid base32 characters."""
    return all(c in VALID_CHARS for c in term)

def validate_end_chars(term, exclude_last=False):
    """Validate if a term can appear at the end of an Algorand address."""
    if not term:
        return False, "Empty term"
    
    if not exclude_last:
        last_char = term[-1]
        if last_char not in VALID_END_CHARS:
            valid_ends = ", ".join(sorted(VALID_END_CHARS))
            return False, f"Warning: Address can only end with these characters: {valid_ends}"
    return True, None

def display_pattern_visual(terms, nums, positions, exclude_lasts):
    print("\nSearching for addresses with these patterns:")
    print("-" * 70)
    
    i = 0
    while i < len(terms):
        pattern = ["#"] * ALGORAND_ADDRESS_LENGTH
        
        if i+1 < len(positions) and positions[i] == "F" and positions[i+1] == "B" and terms[i].startswith("F&B:"):
            front_term = terms[i][4:]
            back_term = terms[i+1]
            pattern[:len(front_term)] = front_term
            if exclude_lasts[i+1]:
                pattern[-len(back_term)-1:-1] = back_term
            else:
                pattern[-len(back_term):] = back_term
            print(f"Front & Back: {''.join(pattern)}")
            i += 2
        else:
            if positions[i] == "F":
                pattern[:len(terms[i])] = terms[i]
                print(f"Front:       {''.join(pattern)}")
            elif positions[i] == "B":
                if exclude_lasts[i]:
                    pattern[-len(terms[i])-1:-1] = terms[i]
                    print(f"Back (excluding last): {''.join(pattern)}")
                else:
                    pattern[-len(terms[i]):] = terms[i]
                    print(f"Back:        {''.join(pattern)}")
            elif positions[i] == "A":
                print(f"Anywhere:    {terms[i]} (can appear anywhere in address)")
            i += 1
    print("-" * 70)

def display_match(term, address, passphrase, found_count, exclude_last=False):
    print("\n" + "="*70)
    print(f"Match #{found_count}".center(70))
    print("="*70)
    print(f"Pattern: {term}")
    print("-"*70)
    print(f"Address:    {address}")
    if exclude_last:
        pattern = ['#'] * ALGORAND_ADDRESS_LENGTH
        pattern[-len(term)-1:-1] = term
        print(f"Pattern:    {''.join(pattern)}")
    else:
        print(f"Pattern:    {'#'*(ALGORAND_ADDRESS_LENGTH-len(term))}{term}")
    print(f"Passphrase: {passphrase}")
    print("="*70)

def display_search_terms(terms, nums, positions, exclude_lasts, total_addresses):
    print("\n" + "="*60)
    print("Current Search Terms".center(60))
    print("="*60)
    print("Total Addresses to Check: {:,}".format(total_addresses))
    print("="*60)
    print("| {:<15} | {:<8} | {:<25} |".format("String", "Length", "Location"))
    print("-"*60)
    
    i = 0
    while i < len(terms):
        if i+1 < len(positions) and positions[i] == "F" and positions[i+1] == "B" and terms[i].startswith("F&B:"):
            combined_term = terms[i][4:] + " & " + terms[i+1]
            location = "Front & Back"
            if exclude_lasts[i+1]:
                location += " (excl. last)"
            print("| {:<15} | {:<8} | {:<25} |".format(
                combined_term, 
                f"{nums[i]},{nums[i+1]}", 
                location
            ))
            i += 2
        else:
            location = {
                "F": "Front",
                "B": "Back",
                "A": "Anywhere"
            }.get(positions[i], positions[i])
            if positions[i] == "B" and exclude_lasts[i]:
                location += " (excl. last)"
            print("| {:<15} | {:<8} | {:<25} |".format(
                terms[i], 
                nums[i], 
                location
            ))
            i += 1
    print("="*60)
    
    if any(pos == "B" for pos in positions) or any(pos == "FB" for pos in positions):
        print("\nReminder: Valid end characters are:", ", ".join(sorted(VALID_END_CHARS)))
        print("="*60)

def search_address(address, terms, nums, positions, exclude_lasts):
    i = 0
    while i < len(terms):
        if i+1 < len(positions) and positions[i] == "F" and positions[i+1] == "B" and terms[i].startswith("F&B:"):
            front_term = terms[i][4:]
            back_term = terms[i+1]
            if exclude_lasts[i+1]:
                if (address[:len(front_term)] == front_term and 
                    address[-len(back_term)-1:-1] == back_term):
                    return True, f"{front_term} & {back_term} (excl. last)"
            else:
                if (address[:len(front_term)] == front_term and 
                    address[-len(back_term):] == back_term):
                    return True, f"{front_term} & {back_term}"
            i += 2
        else:
            term_len = len(terms[i])
            if positions[i] == "A" and terms[i] in address:
                return True, terms[i]
            elif positions[i] == "F" and address[:term_len] == terms[i]:
                return True, terms[i]
            elif positions[i] == "B":
                if exclude_lasts[i]:
                    if address[-term_len-1:-1] == terms[i]:
                        return True, f"{terms[i]} (excl. last)"
                else:
                    if address[-term_len:] == terms[i]:
                        return True, terms[i]
            i += 1
    return False, None

def get_number_input(prompt):
    """Helper function to get valid number input."""
    while True:
        try:
            num = int(input(prompt))
            if num <= 0:
                print("Please enter a positive number.")
                continue
            return num
        except ValueError:
            print("Please enter a valid number.")

def get_search_terms(total_addresses):
    terms = []
    nums = []
    positions = []
    exclude_lasts = []
    
    print("\nWould you like to:")
    print("1. Load default search terms (searchAlgo.json)")
    print("2. Load search terms from a custom file")
    print("3. Enter search terms manually")
    
    while True:
        choice = input("\nEnter your choice (1, 2 or 3): ")
        if choice in ["1", "2", "3"]:
            break
        print("Please enter 1, 2, or 3.")
    
    if choice in ["1", "2"]:
        if choice == "1":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(script_dir, "searchAlgo.json")
        else:
            filename = input("\nEnter the path to your search terms file (or press Enter to skip): ").strip()
            if not filename:
                print("\nFalling back to manual entry...")
                choice = "3"
        
        if choice != "3":
            try:
                if not os.path.exists(filename):
                    print(f"Error: File '{filename}' not found.")
                    print("\nFalling back to manual entry...")
                else:
                    with open(filename, 'r') as f:
                        data = json.load(f)
                        
                    if "search_terms" not in data:
                        print("Error: File must contain a 'search_terms' array.")
                        print("\nFalling back to manual entry...")
                    else:
                        terms = []
                        nums = []
                        positions = []
                        exclude_lasts = []
                        
                        for term_data in data["search_terms"]:
                            if term_data["position"] == "FB":
                                # Add the F&B: prefix to mark it as a combined search
                                terms.extend([f"F&B:{term_data['front_term']}", term_data['back_term']])
                                nums.extend([term_data['front_digits'], term_data['back_digits']])
                                positions.extend(["F", "B"])
                                # Use the exclude_last value from the JSON
                                exclude_lasts.extend([False, term_data.get('exclude_last', False)])
                            else:
                                terms.append(term_data["term"])
                                nums.append(term_data["digits"])
                                positions.append(term_data["position"])
                                exclude_lasts.append(term_data.get("exclude_last", False))
                        
                        # Validate the loaded terms
                        valid_terms = True
                        for i, (term, num, pos) in enumerate(zip(terms, nums, positions)):
                            term_to_check = term[4:] if term.startswith("F&B:") else term
                            if not validate_search_term(term_to_check):
                                print(f"Error: Invalid characters in term '{term_to_check}'")
                                valid_terms = False
                                break
                                
                            if len(term_to_check) != num:
                                print(f"Error: Term '{term_to_check}' length doesn't match specified digits {num}")
                                valid_terms = False
                                break
                                
                            # Only validate end chars for standalone back positions
                            if pos == "B" and not exclude_lasts[i] and not any(t.startswith("F&B:") for t in terms[max(0, i-1):i+1]):
                                valid, message = validate_end_chars(term)
                                if not valid:
                                    print(f"Error in term '{term}': {message}")
                                    valid_terms = False
                                    break
                        
                        if valid_terms:
                            display_search_terms(terms, nums, positions, exclude_lasts, total_addresses)
                            return terms, nums, positions, exclude_lasts
                        
                        print("\nFalling back to manual entry...")
                        terms = []
                        nums = []
                        positions = []
                        exclude_lasts = []
                        
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in file.")
                print("\nFalling back to manual entry...")
            except KeyError as e:
                print(f"Error: Missing required field {e} in search terms file.")
                print("\nFalling back to manual entry...")
            except Exception as e:
                print(f"Error loading file: {str(e)}")
                print("\nFalling back to manual entry...")
    
    while True:
        print("\nSearch Locations:")
        print("F - Front of address")
        print("B - Back of address")
        print("A - Anywhere in address")
        print("FB - Front & Back combination")
        
        while True:
            pos = str.upper(input("\nSelect search location (F/B/A/FB): \n"))
            if pos not in ["F", "B", "A", "FB"]:
                print("Invalid selection. Please choose F, B, A, or FB.")
                continue
            break
        
        exclude_last = False
        if pos in ["B", "FB"]:
            exclude = input("Exclude last character? (Y/N): ").upper()
            exclude_last = exclude == "Y"

        if pos == "F":
            num = get_number_input("Enter number of characters to search at the front: \n")
        elif pos == "B":
            num = get_number_input("Enter number of characters to search at the back: \n")
        elif pos == "A":
            num = get_number_input("Enter number of characters to search for: \n")
        else:  # FB
            num = get_number_input("Enter number of characters to search at the front: \n")
        
        while True:
            searchterm = str(input(f"Enter {num} character(s): \n")).upper()
            if not validate_search_term(searchterm):
                print(f"Error: Invalid characters detected. Only use: {sorted(VALID_CHARS)}")
                continue
            
            if len(searchterm) != num:
                print(f"Error: Please enter exactly {num} characters.")
                continue
            
            if pos == "FB":
                bnum = get_number_input("Enter number of characters to search at the back: \n")
                while True:
                    bterm = str(input(f"Enter {bnum} character(s): \n")).upper()
                    if not validate_search_term(bterm):
                        print(f"Error: Invalid characters detected. Only use: {sorted(VALID_CHARS)}")
                        continue
                    if len(bterm) != bnum:
                        print(f"Error: Please enter exactly {bnum} characters.")
                        continue
                    if not exclude_last:  # Only validate end chars if not excluding last
                        valid, message = validate_end_chars(bterm)
                        if not valid:
                            print(message)
                            continue
                    break
                
                terms.extend([f"F&B:{searchterm}", bterm])
                nums.extend([num, bnum])
                positions.extend(["F", "B"])
                exclude_lasts.extend([False, exclude_last])
            else:
                if pos == "B" and not exclude_last:
                    valid, message = validate_end_chars(searchterm)
                    if not valid:
                        print(message)
                        continue
                terms.append(searchterm)
                nums.append(num)
                positions.append(pos)
                exclude_lasts.append(exclude_last)
            break
        
        display_search_terms(terms, nums, positions, exclude_lasts, total_addresses)
        
        # Show end character reminder if needed
        has_back_patterns = any(
            (pos == "B" or (pos == "FB" and i % 2 == 1)) and not excl 
            for i, (pos, excl) in enumerate(zip(positions, exclude_lasts))
        )
        if has_back_patterns:
            print("\nReminder: Valid end characters are:", ", ".join(sorted(VALID_END_CHARS)))
            print("="*60)
        
        while True:
            add_more = str.upper(input("Do you want to add another search term? (Y)es or (N)o: \n"))
            if add_more in ["Y", "N"]:
                break
            print("Please enter Y or N.")
            
        if add_more != "Y":
            break
            
    return terms, nums, positions, exclude_lasts
    
    
    
def main():
    display_logo()
    
    while True:
        try:
            total_addresses = get_number_input("Please enter the number of Algorand keypairs to generate: \n")
            break
        except ValueError:
            print("Please enter a valid number.")

    searchterms, nums, positions, exclude_lasts = get_search_terms(total_addresses)
    
    display_pattern_visual(searchterms, nums, positions, exclude_lasts)
    print("\nSearching for addresses... Press Ctrl+C to stop")
    found_addresses = 0
    checked_addresses = 0
    matches_by_pattern = {}

    with tqdm(total=total_addresses, desc="Generating addresses", unit="addr") as pbar:
        while checked_addresses < total_addresses:
            private_key, address = account.generate_account()
            checked_addresses += 1
            
            found, matched_term = search_address(address, searchterms, nums, positions, exclude_lasts)
            if found:
                found_addresses += 1
                matches_by_pattern[matched_term] = matches_by_pattern.get(matched_term, 0) + 1
                
                # Determine if this match used exclude_last
                exclude_last = "excl. last" in matched_term
                display_match(matched_term.replace(" (excl. last)", ""), 
                            address, 
                            mnemonic.from_private_key(private_key), 
                            found_addresses,
                            exclude_last)
                
            pbar.update(1)

        print("\n" + "="*50)
        print("Search Complete!".center(50))
        print("="*50)
        print(f"Total Addresses Checked: {checked_addresses:,}")
        print(f"Total Matches Found: {found_addresses:,}")
        print("-"*50)
        print("Matches by Pattern:")
        for pattern, count in matches_by_pattern.items():
            print(f"  {pattern}: {count}")
        print("="*50)

if __name__ == "__main__":
    main()
