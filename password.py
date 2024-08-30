import random
import string
import pyperclip

def generate_password(length, use_uppercase, use_digits, use_symbols):
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ''
    digits = string.digits if use_digits else ''
    symbols = string.punctuation if use_symbols else ''
    
    # Combine all character sets
    all_characters = lowercase + uppercase + digits + symbols
    
    if not all_characters:
        raise ValueError("No character set selected. Please choose at least one option.")
    
    # Generate password
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

def main():
    print("Welcome to the Password Generator!")
    
    try:
        length = int(input("Enter the desired password length: "))
        use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
        
        # Generate the password
        password = generate_password(length, use_uppercase, use_digits, use_symbols)
        
        # Display the password
        print(f"Generated password: {password}")
        
        # Copy to clipboard option
        copy_to_clipboard = input("Copy password to clipboard? (y/n): ").lower() == 'y'
        if copy_to_clipboard:
            pyperclip.copy(password)
            print("Password copied to clipboard.")
        else:
            print("Password not copied.")
    
    except ValueError as ve:
        print(f"Error: {ve}")

if __name__ == "__main__":
    main()