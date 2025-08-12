#!/usr/bin/env python3
"""
🔤 ADVANCED WORDLIST GENERATOR
==============================
Generate sophisticated password lists for security testing.
ONLY use on networks you own or have explicit permission to test.

Features:
- SSID-based password generation
- Keyboard pattern analysis
- Date and number sequence generation
- Dictionary mutations
- Brute force combinations
- Statistical analysis of password patterns
"""

import itertools
import string
import re
import calendar
from datetime import datetime, timedelta
import random

class AdvancedWordlistGenerator:
    def __init__(self):
        self.generated_passwords = set()
        self.stats = {
            'total_generated': 0,
            'unique_passwords': 0,
            'pattern_distribution': {}
        }
    
    def generate_ssid_variants(self, ssid):
        """Generate SSID-based password variants"""
        variants = []
        ssid_clean = re.sub(r'[^a-zA-Z0-9]', '', ssid)
        
        # Basic transformations
        base_variants = [
            ssid, ssid.lower(), ssid.upper(), ssid.capitalize(),
            ssid_clean, ssid_clean.lower(), ssid_clean.upper(),
        ]
        
        # Add common suffixes/prefixes
        suffixes = ['123', '2025', '2024', '2023', 'wifi', 'net', 'home', 
                   'password', '!', '@', '#', '1', '12', '01', '00']
        prefixes = ['wifi', 'my', 'home', 'net', 'the', '']
        
        for base in base_variants:
            if base:  # Skip empty strings
                variants.append(base)
                for suffix in suffixes:
                    variants.append(base + suffix)
                    variants.append(base + suffix.upper())
                for prefix in prefixes:
                    if prefix:
                        variants.append(prefix + base)
                        variants.append(prefix.upper() + base)
        
        return list(set(variants))
    
    def generate_keyboard_patterns(self):
        """Generate keyboard walk patterns"""
        patterns = []
        
        # QWERTY rows
        qwerty_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm'
        ]
        
        # Generate patterns of different lengths
        for row in qwerty_rows:
            for start in range(len(row)):
                for length in range(4, min(len(row) - start + 1, 13)):
                    pattern = row[start:start + length]
                    patterns.append(pattern)
                    patterns.append(pattern.upper())
                    patterns.append(pattern.capitalize())
                    # Add numbers
                    patterns.append(pattern + '123')
                    patterns.append(pattern + '2025')
        
        # Diagonal patterns
        diagonal_patterns = [
            'qaz', 'wsx', 'edc', 'rfv', 'tgb', 'yhn', 'ujm',
            '1qaz', '2wsx', '3edc', '4rfv', '5tgb', '6yhn', '7ujm',
            'qazwsx', 'wsxedc', 'edcrfv', 'rfvtgb', 'tgbyhn', 'yhnujm',
        ]
        
        for pattern in diagonal_patterns:
            patterns.append(pattern)
            patterns.append(pattern.upper())
            patterns.append(pattern + '123')
        
        return patterns
    
    def generate_date_patterns(self, years_back=10, years_forward=2):
        """Generate date-based passwords"""
        patterns = []
        current_year = datetime.now().year
        
        # Year patterns
        for year in range(current_year - years_back, current_year + years_forward):
            patterns.extend([
                str(year),
                str(year)[2:],  # Last 2 digits
                str(year) + str(year),  # Double year
                'password' + str(year),
                'wifi' + str(year),
                str(year) + 'password',
                str(year) + 'wifi',
            ])
        
        # Month/Day patterns
        for month in range(1, 13):
            patterns.extend([
                f"{month:02d}{current_year}",
                f"{month:02d}{str(current_year)[2:]}",
                f"{calendar.month_name[month].lower()}{current_year}",
                f"{calendar.month_abbr[month].lower()}{current_year}",
            ])
        
        # Common date formats
        common_dates = [
            '01012000', '12312000', '01011990', '12311990',
            '01012025', '12312025', '01011980', '12311980',
            '01011970', '12311970', '01012024', '12312024',
        ]
        patterns.extend(common_dates)
        
        return patterns
    
    def generate_number_sequences(self, min_length=6, max_length=12):
        """Generate number sequence patterns"""
        patterns = []
        
        # Sequential patterns
        for length in range(min_length, max_length + 1):
            # Ascending
            ascending = ''.join([str(i % 10) for i in range(1, length + 1)])
            patterns.append(ascending)
            
            # Descending
            descending = ''.join([str(i % 10) for i in range(length, 0, -1)])
            patterns.append(descending)
            
            # Repeating digits
            for digit in '0123456789':
                patterns.append(digit * length)
            
            # Alternating patterns
            patterns.append('12' * (length // 2) + ('1' if length % 2 else ''))
            patterns.append('01' * (length // 2) + ('0' if length % 2 else ''))
            
        # Phone number patterns
        phone_patterns = [
            '5551234567', '1234567890', '0123456789',
            '5555555555', '1111111111', '9999999999',
            '8005551234', '4155551234', '2125551234',
        ]
        patterns.extend(phone_patterns)
        
        return patterns
    
    def generate_dictionary_mutations(self, base_words=None):
        """Generate mutations of dictionary words"""
        if base_words is None:
            base_words = [
                # Common words
                'password', 'admin', 'user', 'guest', 'root',
                'wifi', 'internet', 'network', 'wireless', 'router',
                'home', 'office', 'computer', 'laptop', 'phone',
                'love', 'family', 'work', 'school', 'house',
                'secret', 'private', 'secure', 'safe', 'hidden',
                
                # Tech terms
                'server', 'database', 'system', 'access', 'login',
                'default', 'public', 'private', 'local', 'remote',
                'backup', 'config', 'setup', 'install', 'update',
                
                # Places
                'america', 'california', 'newyork', 'london', 'tokyo',
                'home', 'office', 'school', 'work', 'house',
            ]
        
        mutations = []
        
        # Character substitutions
        substitutions = {
            'a': ['@', '4'], 'e': ['3'], 'i': ['1', '!'], 'o': ['0'],
            's': ['$', '5'], 't': ['7'], 'l': ['1'], 'g': ['9']
        }
        
        for word in base_words:
            # Basic transformations
            mutations.extend([
                word, word.upper(), word.capitalize(),
                word.title(), word.swapcase()
            ])
            
            # Add numbers and symbols
            for suffix in ['123', '2025', '!', '@', '#', '1', '12', '01']:
                mutations.append(word + suffix)
                mutations.append(word.capitalize() + suffix)
                mutations.append(word.upper() + suffix)
            
            for prefix in ['my', 'the', '1', '@']:
                mutations.append(prefix + word)
                mutations.append(prefix + word.capitalize())
            
            # Character substitutions
            mutated = word
            for char, subs in substitutions.items():
                for sub in subs:
                    mutated_word = word.replace(char, sub)
                    if mutated_word != word:
                        mutations.append(mutated_word)
                        mutations.append(mutated_word.capitalize())
        
        return list(set(mutations))
    
    def generate_brute_force_samples(self, charset_type='mixed', min_length=4, max_length=8, sample_size=1000):
        """Generate brute force password samples"""
        if charset_type == 'numeric':
            charset = string.digits
        elif charset_type == 'lowercase':
            charset = string.ascii_lowercase
        elif charset_type == 'uppercase':
            charset = string.ascii_uppercase
        elif charset_type == 'alpha':
            charset = string.ascii_letters
        elif charset_type == 'mixed':
            charset = string.ascii_letters + string.digits
        elif charset_type == 'full':
            charset = string.ascii_letters + string.digits + '!@#$%^&*()_+-='
        else:
            charset = string.ascii_letters + string.digits
        
        samples = []
        
        # For shorter lengths, generate systematically
        for length in range(min_length, min(max_length + 1, 6)):
            count = 0
            for password in itertools.product(charset, repeat=length):
                samples.append(''.join(password))
                count += 1
                if count >= sample_size // (max_length - min_length + 1):
                    break
        
        # For longer lengths, generate random samples
        for length in range(6, max_length + 1):
            for _ in range(sample_size // (max_length - min_length + 1)):
                password = ''.join(random.choices(charset, k=length))
                samples.append(password)
        
        return samples[:sample_size]
    
    def generate_company_patterns(self, company_keywords=None):
        """Generate company/organization specific patterns"""
        if company_keywords is None:
            company_keywords = [
                'company', 'corp', 'inc', 'ltd', 'llc', 'group',
                'tech', 'solutions', 'services', 'systems', 'net',
                'wireless', 'telecom', 'internet', 'broadband',
            ]
        
        patterns = []
        current_year = datetime.now().year
        
        for keyword in company_keywords:
            patterns.extend([
                keyword, keyword.upper(), keyword.capitalize(),
                keyword + '123', keyword + str(current_year),
                keyword + 'wifi', keyword + 'net',
                'guest' + keyword, keyword + 'guest',
                'admin' + keyword, keyword + 'admin',
            ])
        
        return patterns
    
    def analyze_password_strength(self, password):
        """Analyze password strength and categorize"""
        analysis = {
            'length': len(password),
            'has_uppercase': bool(re.search(r'[A-Z]', password)),
            'has_lowercase': bool(re.search(r'[a-z]', password)),
            'has_digits': bool(re.search(r'\d', password)),
            'has_symbols': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>?]', password)),
            'pattern_type': 'unknown'
        }
        
        # Categorize pattern type
        if password.isdigit():
            analysis['pattern_type'] = 'numeric'
        elif password.isalpha():
            analysis['pattern_type'] = 'alphabetic'
        elif re.match(r'^[a-zA-Z0-9]+$', password):
            analysis['pattern_type'] = 'alphanumeric'
        elif any(char in string.punctuation for char in password):
            analysis['pattern_type'] = 'complex'
        
        # Calculate strength score
        score = 0
        score += min(analysis['length'] * 2, 20)  # Length (max 20)
        score += 10 if analysis['has_uppercase'] else 0
        score += 10 if analysis['has_lowercase'] else 0
        score += 15 if analysis['has_digits'] else 0
        score += 20 if analysis['has_symbols'] else 0
        
        analysis['strength_score'] = score
        if score < 30:
            analysis['strength_level'] = 'very_weak'
        elif score < 50:
            analysis['strength_level'] = 'weak'
        elif score < 70:
            analysis['strength_level'] = 'medium'
        elif score < 90:
            analysis['strength_level'] = 'strong'
        else:
            analysis['strength_level'] = 'very_strong'
        
        return analysis
    
    def generate_comprehensive_wordlist(self, target_ssid=None, max_passwords=10000, include_patterns=None):
        """Generate comprehensive wordlist with multiple strategies"""
        if include_patterns is None:
            include_patterns = ['ssid', 'keyboard', 'dates', 'numbers', 'dictionary', 'company']
        
        all_passwords = []
        
        print("🎯 Generating comprehensive wordlist...")
        
        # SSID-based patterns
        if 'ssid' in include_patterns and target_ssid:
            print("  📡 Generating SSID variants...")
            ssid_variants = self.generate_ssid_variants(target_ssid)
            all_passwords.extend(ssid_variants)
            print(f"     Generated {len(ssid_variants)} SSID variants")
        
        # Keyboard patterns
        if 'keyboard' in include_patterns:
            print("  ⌨️  Generating keyboard patterns...")
            keyboard_patterns = self.generate_keyboard_patterns()
            all_passwords.extend(keyboard_patterns)
            print(f"     Generated {len(keyboard_patterns)} keyboard patterns")
        
        # Date patterns
        if 'dates' in include_patterns:
            print("  📅 Generating date patterns...")
            date_patterns = self.generate_date_patterns()
            all_passwords.extend(date_patterns)
            print(f"     Generated {len(date_patterns)} date patterns")
        
        # Number sequences
        if 'numbers' in include_patterns:
            print("  🔢 Generating number sequences...")
            number_patterns = self.generate_number_sequences()
            all_passwords.extend(number_patterns)
            print(f"     Generated {len(number_patterns)} number patterns")
        
        # Dictionary mutations
        if 'dictionary' in include_patterns:
            print("  📚 Generating dictionary mutations...")
            dict_mutations = self.generate_dictionary_mutations()
            all_passwords.extend(dict_mutations)
            print(f"     Generated {len(dict_mutations)} dictionary mutations")
        
        # Company patterns
        if 'company' in include_patterns:
            print("  🏢 Generating company patterns...")
            company_patterns = self.generate_company_patterns()
            all_passwords.extend(company_patterns)
            print(f"     Generated {len(company_patterns)} company patterns")
        
        # Remove duplicates and filter
        unique_passwords = list(dict.fromkeys(all_passwords))  # Preserve order
        filtered_passwords = [p for p in unique_passwords if 4 <= len(p) <= 63]
        
        # Limit to max_passwords
        final_passwords = filtered_passwords[:max_passwords]
        
        # Update stats
        self.stats['total_generated'] = len(all_passwords)
        self.stats['unique_passwords'] = len(final_passwords)
        
        # Analyze patterns
        pattern_distribution = {}
        for password in final_passwords[:1000]:  # Analyze sample
            analysis = self.analyze_password_strength(password)
            pattern_type = analysis['pattern_type']
            pattern_distribution[pattern_type] = pattern_distribution.get(pattern_type, 0) + 1
        
        self.stats['pattern_distribution'] = pattern_distribution
        
        print(f"\n✅ Wordlist generation complete!")
        print(f"   📊 Total generated: {self.stats['total_generated']:,}")
        print(f"   🎯 Unique passwords: {self.stats['unique_passwords']:,}")
        print(f"   📈 Pattern distribution: {pattern_distribution}")
        
        return final_passwords
    
    def save_wordlist(self, passwords, filename):
        """Save wordlist to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for password in passwords:
                    f.write(password + '\n')
            print(f"💾 Wordlist saved to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving wordlist: {e}")
            return False
    
    def load_wordlist(self, filename):
        """Load wordlist from file"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            print(f"📂 Loaded {len(passwords)} passwords from: {filename}")
            return passwords
        except Exception as e:
            print(f"❌ Error loading wordlist: {e}")
            return []

def main():
    """Main function for standalone usage"""
    print("🔤 Advanced Wordlist Generator")
    print("=" * 40)
    
    generator = AdvancedWordlistGenerator()
    
    # Interactive mode
    target_ssid = input("Enter target SSID (or press Enter to skip): ").strip()
    if not target_ssid:
        target_ssid = None
    
    max_passwords = input("Maximum passwords to generate (default 5000): ").strip()
    try:
        max_passwords = int(max_passwords) if max_passwords else 5000
    except ValueError:
        max_passwords = 5000
    
    # Generate wordlist
    passwords = generator.generate_comprehensive_wordlist(
        target_ssid=target_ssid,
        max_passwords=max_passwords
    )
    
    # Save option
    save_option = input("\nSave wordlist to file? (y/n): ").strip().lower()
    if save_option in ['y', 'yes']:
        filename = input("Enter filename (default: wordlist.txt): ").strip()
        if not filename:
            filename = "wordlist.txt"
        generator.save_wordlist(passwords, filename)
    
    # Show sample
    print(f"\n📝 Sample passwords (first 20):")
    for i, password in enumerate(passwords[:20], 1):
        analysis = generator.analyze_password_strength(password)
        print(f"   {i:2d}. {password:<15} ({analysis['strength_level']}, {analysis['length']} chars)")

if __name__ == "__main__":
    main()
