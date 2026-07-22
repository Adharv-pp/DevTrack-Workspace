import re

def devtrack_registration():
    print("=== DevTrack Registration Gateway ===")
    print("Type 'exit' at any time to cancel.\n")

    # 1. Full Name Validation (using re.findall) - Replaces the Skills input
    while True:
        name = input("1. Enter Full Name (First & Last): ")
        if name.lower() == 'exit': return
        
        # Extracts all alphabetical words into a list
        name_parts = re.findall(r"[A-Za-z]+", name)
        
        # Checks if there are at least 2 words (First and Last name)
        if len(name_parts) >= 2:
            break
        print(" Error: Please enter both a first and last name.\n")

    # 2. Developer ID Validation (using re.match)
    while True:
        dev_id = input("2. Enter DevID (Format: DEV-XXX): ")
        if dev_id.lower() == 'exit': return
        
        if re.match(r"^DEV-\d{3}$", dev_id):
            break
        print(" Error: Must start with 'DEV-' followed exactly by 3 numbers.\n")

    # 3. Username Validation (using re.fullmatch)
    while True:
        username = input("3. Enter Username (5-10 lowercase letters/numbers): ")
        if username.lower() == 'exit': return
        
        if re.fullmatch(r"[a-z0-9]{5,10}", username):
            break
        print(" Error: Must be 5-10 characters long, using only lowercase letters/numbers.\n")

    # 4. Password Validation (using re.search)
    while True:
        password = input("4. Enter Password (needs 1 special character): ")
        if password.lower() == 'exit': return
        
        if re.search(r"[@_!#$%^&*]", password):
            break
        print(" Error: Password must contain at least one special character.\n")

    # 5. Phone Number Validation (using re.sub)
    while True:
        phone = input("5. Enter Phone Number: ")
        if phone.lower() == 'exit': return
        
        # Replaces anything that is NOT a number (\D) with nothing ("")
        clean_phone = re.sub(r"\D", "", phone) 
        
        if len(clean_phone) >= 10:
            break
        print(" Error: Please enter a valid phone number with at least 10 digits.\n")

    # Success Output
    print("\n✅ All inputs validated successfully!")
    print(f"Welcome to DevTrack, {name_parts[0]} ({dev_id})!")

if __name__ == "__main__":
    devtrack_registration()