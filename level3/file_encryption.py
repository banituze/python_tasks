#!/usr/bin/env python3
"""
Level 3 Task 2: Basic File Encryption/Decryption
A Python script that encrypts and decrypts text files using multiple algorithms.
"""

import os
import base64
import getpass
import hashlib
from typing import Optional, Tuple

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    print(" Cryptography library not found. Install with: pip install cryptography")

class CaesarCipher:
    """Caesar cipher implementation"""
    
    @staticmethod
    def encrypt(text: str, shift: int = 13) -> str:
        """Encrypt text using Caesar cipher"""
        result = ""
        shift = shift % 26  # Ensure shift is within 0-25 range
        
        for char in text:
            if char.isalpha():
                # Determine if uppercase or lowercase
                base = ord('A') if char.isupper() else ord('a')
                # Apply Caesar shift
                shifted = (ord(char) - base + shift) % 26
                result += chr(base + shifted)
            else:
                # Non-alphabetic characters remain unchanged
                result += char
        
        return result
    
    @staticmethod
    def decrypt(text: str, shift: int = 13) -> str:
        """Decrypt text using Caesar cipher"""
        # Decryption is encryption with negative shift
        return CaesarCipher.encrypt(text, -shift)
    
    @staticmethod
    def brute_force_decrypt(text: str) -> list:
        """Try all possible shifts to decrypt Caesar cipher"""
        results = []
        for shift in range(26):
            decrypted = CaesarCipher.decrypt(text, shift)
            results.append((shift, decrypted))
        return results

class FernetEncryption:
    """Fernet encryption implementation using cryptography library"""
    
    def __init__(self):
        self.key = None
        self.fernet = None
    
    def generate_key_from_password(self, password: str, salt: bytes = None) -> bytes:
        """Generate Fernet key from password using PBKDF2"""
        if not CRYPTOGRAPHY_AVAILABLE:
            raise ImportError("Cryptography library is required for Fernet encryption")
        
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key
        self.fernet = Fernet(key)
        return salt
    
    def load_key_from_password(self, password: str, salt: bytes) -> None:
        """Load Fernet key from password and salt"""
        if not CRYPTOGRAPHY_AVAILABLE:
            raise ImportError("Cryptography library is required for Fernet encryption")
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key
        self.fernet = Fernet(key)
    
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using Fernet"""
        if not self.fernet:
            raise ValueError("Encryption key not set")
        return self.fernet.encrypt(data)
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Decrypt data using Fernet"""
        if not self.fernet:
            raise ValueError("Encryption key not set")
        return self.fernet.decrypt(encrypted_data)

class FileEncryption:
    """Main file encryption/decryption class"""
    
    def __init__(self):
        self.caesar = CaesarCipher()
        self.fernet_enc = FernetEncryption()
    
    def validate_file_path(self, file_path: str) -> bool:
        """Validate if file exists and is readable"""
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    
    def read_file(self, file_path: str) -> Tuple[bytes, str]:
        """Read file content and detect encoding"""
        try:
            # Try to read as text first (UTF-8)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content.encode('utf-8'), 'text'
        except UnicodeDecodeError:
            # If UTF-8 fails, read as binary
            with open(file_path, 'rb') as file:
                content = file.read()
                return content, 'binary'
    
    def write_file(self, file_path: str, content: bytes, is_text: bool = True):
        """Write content to file"""
        if is_text:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content.decode('utf-8'))
        else:
            with open(file_path, 'wb') as file:
                file.write(content)
    
    def encrypt_file_caesar(self, input_file: str, output_file: str, shift: int = 13):
        """Encrypt file using Caesar cipher"""
        try:
            content, file_type = self.read_file(input_file)
            
            if file_type == 'binary':
                print(" Caesar cipher works best with text files. Binary files may not encrypt properly.")
            
            text_content = content.decode('utf-8', errors='ignore')
            encrypted_content = self.caesar.encrypt(text_content, shift)
            
            self.write_file(output_file, encrypted_content.encode('utf-8'), True)
            print(f" File encrypted with Caesar cipher (shift={shift}): {output_file}")
            
            # Save encryption info
            info_file = output_file + ".caesar_info"
            with open(info_file, 'w') as f:
                f.write(f"algorithm:caesar\nshift:{shift}\noriginal_file:{input_file}\n")
            print(f" Encryption info saved: {info_file}")
            
        except Exception as e:
            print(f" Error encrypting file: {e}")
    
    def decrypt_file_caesar(self, input_file: str, output_file: str, shift: int = None):
        """Decrypt file using Caesar cipher"""
        try:
            # Try to read encryption info
            info_file = input_file + ".caesar_info"
            if shift is None and os.path.exists(info_file):
                with open(info_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith('shift:'):
                            shift = int(line.split(':')[1].strip())
                            print(f" Found shift value in info file: {shift}")
                            break
            
            if shift is None:
                print(" No shift value provided. Trying brute force decryption...")
                content, _ = self.read_file(input_file)
                text_content = content.decode('utf-8', errors='ignore')
                
                results = self.caesar.brute_force_decrypt(text_content)
                print("\n Brute force decryption results (first 100 chars of each):")
                print("-" * 60)
                for shift_val, decrypted in results:
                    preview = decrypted[:100].replace('\n', ' ')
                    print(f"Shift {shift_val:2d}: {preview}...")
                
                while True:
                    try:
                        shift = int(input("\nEnter the shift value that looks correct: "))
                        if 0 <= shift <= 25:
                            break
                        else:
                            print("Shift must be between 0 and 25")
                    except ValueError:
                        print("Please enter a valid number")
            
            content, _ = self.read_file(input_file)
            text_content = content.decode('utf-8', errors='ignore')
            decrypted_content = self.caesar.decrypt(text_content, shift)
            
            self.write_file(output_file, decrypted_content.encode('utf-8'), True)
            print(f" File decrypted with Caesar cipher: {output_file}")
            
        except Exception as e:
            print(f" Error decrypting file: {e}")
    
    def encrypt_file_fernet(self, input_file: str, output_file: str, password: str = None):
        """Encrypt file using Fernet encryption"""
        if not CRYPTOGRAPHY_AVAILABLE:
            print(" Cryptography library is required for Fernet encryption")
            return
        
        try:
            if password is None:
                password = getpass.getpass("Enter password for encryption: ")
            
            content, file_type = self.read_file(input_file)
            
            # Generate salt and key
            salt = self.fernet_enc.generate_key_from_password(password)
            
            # Encrypt content
            encrypted_content = self.fernet_enc.encrypt(content)
            
            # Write encrypted file
            self.write_file(output_file, encrypted_content, False)
            
            # Save salt for decryption
            salt_file = output_file + ".salt"
            with open(salt_file, 'wb') as f:
                f.write(salt)
            
            # Save encryption info
            info_file = output_file + ".fernet_info"
            with open(info_file, 'w') as f:
                f.write(f"algorithm:fernet\noriginal_file:{input_file}\nfile_type:{file_type}\n")
            
            print(f" File encrypted with Fernet: {output_file}")
            print(f" Salt saved: {salt_file}")
            print(f" Encryption info saved: {info_file}")
            
        except Exception as e:
            print(f" Error encrypting file: {e}")
    
    def decrypt_file_fernet(self, input_file: str, output_file: str, password: str = None):
        """Decrypt file using Fernet encryption"""
        if not CRYPTOGRAPHY_AVAILABLE:
            print(" Cryptography library is required for Fernet encryption")
            return
        
        try:
            if password is None:
                password = getpass.getpass("Enter password for decryption: ")
            
            # Read salt
            salt_file = input_file + ".salt"
            if not os.path.exists(salt_file):
                print(f" Salt file not found: {salt_file}")
                return
            
            with open(salt_file, 'rb') as f:
                salt = f.read()
            
            # Load key
            self.fernet_enc.load_key_from_password(password, salt)
            
            # Read encrypted content
            with open(input_file, 'rb') as f:
                encrypted_content = f.read()
            
            # Decrypt content
            decrypted_content = self.fernet_enc.decrypt(encrypted_content)
            
            # Determine file type from info file
            info_file = input_file + ".fernet_info"
            is_text = True
            if os.path.exists(info_file):
                with open(info_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith('file_type:'):
                            file_type = line.split(':')[1].strip()
                            is_text = (file_type == 'text')
                            break
            
            # Write decrypted content
            self.write_file(output_file, decrypted_content, is_text)
            print(f" File decrypted with Fernet: {output_file}")
            
        except Exception as e:
            print(f" Error decrypting file: {e}")
    
    def create_sample_file(self) -> str:
        """Create a sample text file for testing"""
        sample_content = """This is a sample text file for encryption testing.

It contains multiple lines with various characters:
- Letters (uppercase and lowercase)
- Numbers: 123456789
- Special characters: !@#$%^&*()
- Unicode characters: ñáéíóú 

The quick brown fox jumps over the lazy dog.
This sentence contains every letter of the alphabet.

Encryption algorithms can protect sensitive information
by transforming readable text into unreadable ciphertext.
"""
        
        filename = "sample_text.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        print(f" Sample file created: {filename}")
        return filename

def get_file_path(prompt: str, must_exist: bool = True) -> str:
    """Get file path from user with validation"""
    while True:
        file_path = input(prompt).strip()
        
        if not file_path:
            print("Please enter a file path.")
            continue
        
        if must_exist:
            if os.path.isfile(file_path):
                return file_path
            else:
                print(f" File not found: {file_path}")
        else:
            # For output files, check if directory exists
            dir_path = os.path.dirname(file_path) or '.'
            if os.path.isdir(dir_path):
                return file_path
            else:
                print(f" Directory not found: {dir_path}")

def get_encryption_choice():
    """Get encryption method choice from user"""
    print("\n Choose encryption method:")
    print("1.  Caesar Cipher (simple, educational)")
    print("2.  Fernet Encryption (secure, recommended)")
    
    while True:
        choice = input("Enter your choice (1-2): ").strip()
        if choice in ['1', '2']:
            return choice
        print("Invalid choice. Please enter 1 or 2.")

def get_operation_choice():
    """Get operation choice from user"""
    print("\n Choose operation:")
    print("1.  Encrypt file")
    print("2.  Decrypt file")
    print("3.  Create sample file for testing")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    """Main function"""
    encryptor = FileEncryption()
    
    print(" Welcome to the File Encryption/Decryption Tool!")
    print("This tool supports Caesar cipher and Fernet encryption.")
    print("\n Security Notes:")
    print("- Caesar cipher is NOT secure for real data")
    print("- Fernet encryption is secure for protecting sensitive files")
    print("- Always keep backups of important files")
    print("- Remember your passwords - they cannot be recovered!")
    
    while True:
        operation = get_operation_choice()
        
        try:
            if operation == '3':
                # Create sample file
                sample_file = encryptor.create_sample_file()
                print(f"You can now encrypt/decrypt this file: {sample_file}")
                continue
            
            # Get encryption method
            method = get_encryption_choice()
            
            if operation == '1':
                # Encrypt file
                input_file = get_file_path("Enter path to file to encrypt: ", True)
                
                # Generate output filename
                if method == '1':
                    output_file = input_file + ".caesar_encrypted"
                else:
                    output_file = input_file + ".fernet_encrypted"
                
                custom_output = input(f"Output file [{output_file}]: ").strip()
                if custom_output:
                    output_file = custom_output
                
                if method == '1':
                    # Caesar cipher
                    while True:
                        try:
                            shift = int(input("Enter shift value (1-25, default=13): ") or "13")
                            if 1 <= shift <= 25:
                                break
                            print("Shift must be between 1 and 25")
                        except ValueError:
                            print("Please enter a valid number")
                    
                    encryptor.encrypt_file_caesar(input_file, output_file, shift)
                
                else:
                    # Fernet encryption
                    encryptor.encrypt_file_fernet(input_file, output_file)
            
            elif operation == '2':
                # Decrypt file
                input_file = get_file_path("Enter path to encrypted file: ", True)
                
                # Generate output filename
                base_name = input_file
                for suffix in [".caesar_encrypted", ".fernet_encrypted"]:
                    if input_file.endswith(suffix):
                        base_name = input_file[:-len(suffix)]
                        break
                
                output_file = base_name + ".decrypted"
                custom_output = input(f"Output file [{output_file}]: ").strip()
                if custom_output:
                    output_file = custom_output
                
                if method == '1':
                    # Caesar cipher
                    shift_input = input("Enter shift value (leave empty for auto-detection): ").strip()
                    shift = int(shift_input) if shift_input else None
                    
                    encryptor.decrypt_file_caesar(input_file, output_file, shift)
                
                else:
                    # Fernet encryption
                    encryptor.decrypt_file_fernet(input_file, output_file)
        
        except KeyboardInterrupt:
            print("\n\n Operation cancelled by user")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")
        
        # Ask if user wants to continue
        while True:
            continue_choice = input("\nDo you want to perform another operation? (y/n): ").lower().strip()
            if continue_choice in ['y', 'yes']:
                break
            elif continue_choice in ['n', 'no']:
                print("Thank you for using the File Encryption Tool! ")
                return
            else:
                print("Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()


