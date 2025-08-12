#!/usr/bin/env python3
"""
📝 PASSWORD WORDLIST GENERATOR
=============================
Generate custom wordlists for security testing your own networks.
"""

import itertools
import string
import re
from datetime import datetime

class WordlistGenerator:
    def __init__(self):
        self.common_words = [
            'password', 'admin', 'wifi', 'internet', 'network', 'router',
            'wireless', 'home', 'family', 'house', 'guest', 'office',
            'company', 'business', 'secure', 'private', 'public'
        ]
        
        self.common_numbers = [
            '123', '456', '789', '000', '111', '222', '333', '444', '555',
            '666', '777', '888', '999', '2024', '2025', '2026'
        ]
        
        self.special_chars = ['!', '@', '#', '$', '%', '&', '*', '+', '=']
    
    def generate_common_patterns(self):
        """Generate common password patterns"""
        patterns = []
        
        # Word + Number combinations
        for word in self.common_words:
            for num in self.common_numbers:
                patterns.extend([
                    word + num,
                    num + word,
                    word.capitalize() + num,
                    word.upper() + num
                ])
        
        # Word + Special char combinations
        for word in self.common_words:
            for char in self.special_chars:
                patterns.extend([
                    word + char,
                    word + char + '1',
                    word.capitalize() + char,
                    word + '123' + char
                ])
        
        return patterns
    
    def generate_keyboard_patterns(self):
        """Generate keyboard walk patterns"""
        keyboard_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm',
            '1234567890'
        ]
        
        patterns = []
        
        for row in keyboard_rows:
            # Forward sequences
            for i in range(len(row) - 7):
                patterns.append(row[i:i+8])
                patterns.append(row[i:i+8].upper())
            
            # Reverse sequences
            for i in range(len(row) - 7):
                patterns.append(row[i:i+8][::-1])
        
        # Common keyboard patterns
        common_patterns = [
            'qwerty123', 'asdf1234', 'zxcv1234', '12345678',
            'qwertyui', 'asdfghjk', 'zxcvbnm1', '87654321'
        ]
        
        patterns.extend(common_patterns)
        return patterns
    
    def generate_date_patterns(self):
        """Generate date-based patterns"""
        current_year = datetime.now().year
        patterns = []
        
        # Years
        for year in range(current_year - 5, current_year + 2):
            patterns.extend([
                str(year),
                str(year) * 2,
                'password' + str(year),
                'admin' + str(year),
                str(year) + 'wifi'
            ])
        
        # Months and days
        for month in range(1, 13):
            patterns.extend([
                f'{month:02d}{current_year}',
                f'{current_year}{month:02d}',
                f'password{month:02d}'
            ])
        
        return patterns
    
    def generate_name_based(self, custom_words=None):
        """Generate passwords based on custom words (names, places, etc.)"""
        if not custom_words:
            custom_words = []
        
        patterns = []
        
        for word in custom_words:
            # Basic variations
            patterns.extend([
                word.lower(),
                word.upper(),
                word.capitalize(),
                word + '123',
                word + '2025',
                word + '!',
                word + '@',
                '123' + word,
                word + word,
            ])
            
            # With numbers
            for i in range(10):
                patterns.extend([
                    word + str(i),
                    str(i) + word,
                    word + str(i) * 3
                ])
        
        return patterns
    
    def generate_brute_force(self, charset, min_length=4, max_length=6, max_count=1000):
        """Generate brute force combinations (limited for demo)"""
        patterns = []
        count = 0
        
        for length in range(min_length, max_length + 1):
            for combination in itertools.product(charset, repeat=length):
                if count >= max_count:
                    break
                patterns.append(''.join(combination))
                count += 1
            
            if count >= max_count:
                break
        
        return patterns
    
    def save_wordlist(self, patterns, filename):
        """Save wordlist to file"""
        # Remove duplicates and sort
        unique_patterns = list(set(patterns))
        unique_patterns.sort(key=len)  # Sort by length
        
        with open(filename, 'w') as f:
            for pattern in unique_patterns:
                if 8 <= len(pattern) <= 20:  # Reasonable password length
                    f.write(pattern + '\n')
        
        print(f"📝 Saved {len(unique_patterns)} passwords to {filename}")
        return len(unique_patterns)
    
    def generate_comprehensive_wordlist(self, output_file='custom_wordlist.txt', custom_words=None):
        """Generate a comprehensive wordlist"""
        print("📝 Generating comprehensive wordlist...")
        
        all_patterns = []
        
        # Generate different types of patterns
        print("🔤 Generating common patterns...")
        all_patterns.extend(self.generate_common_patterns())
        
        print("⌨️  Generating keyboard patterns...")
        all_patterns.extend(self.generate_keyboard_patterns())
        
        print("📅 Generating date patterns...")
        all_patterns.extend(self.generate_date_patterns())
        
        if custom_words:
            print("🏷️  Generating name-based patterns...")
            all_patterns.extend(self.generate_name_based(custom_words))
        
        print("🔢 Generating numeric patterns...")
        numeric_charset = string.digits
        all_patterns.extend(self.generate_brute_force(numeric_charset, 8, 10, 100))
        
        print("🔠 Generating limited brute force patterns...")
        simple_charset = string.ascii_lowercase + string.digits
        all_patterns.extend(self.generate_brute_force(simple_charset, 4, 6, 500))
        
        # Save to file
        count = self.save_wordlist(all_patterns, output_file)
        
        print(f"✅ Wordlist generation complete!")
        print(f"📊 Total unique passwords: {count}")
        return output_file

def main():
    """Main function"""
    print("📝 Password Wordlist Generator")
    print("=" * 40)
    print("⚠️  For testing your own networks only!")
    print()
    
    generator = WordlistGenerator()
    
    # Get custom words from user
    custom_words = []
    print("🏷️  Enter custom words (names, places, etc.) one per line.")
    print("   These will be used to generate variations.")
    print("   Press Enter on empty line to finish:")
    
    while True:
        word = input("   Word: ").strip()
        if not word:
            break
        custom_words.append(word)
    
    if custom_words:
        print(f"✅ Added {len(custom_words)} custom words")
    
    # Generate wordlist
    output_file = input("\n📝 Output filename (default: custom_wordlist.txt): ").strip()
    if not output_file:
        output_file = 'custom_wordlist.txt'
    
    generator.generate_comprehensive_wordlist(output_file, custom_words)
    
    print(f"\n💡 Use this wordlist with the network security tester:")
    print(f"   python3 network_security_tester.py")

if __name__ == "__main__":
    main()
