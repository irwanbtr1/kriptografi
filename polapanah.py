import os

class ArrowCipher:
    def __init__(self, depth=4):
        """
        Inisialisasi cipher dengan kedalaman panah
        depth: jumlah baris dalam pola panah (default 4)
        """
        self.depth = depth
    
    def encrypt_text(self, plaintext):
        """
        Enkripsi teks menggunakan pola panah (zigzag)
        """
        if len(plaintext) <= 1:
            return plaintext
        
        # Hilangkan spasi dan ubah ke uppercase
        text = plaintext.replace(" ", "").upper()
        
        # Buat array untuk setiap baris
        rows = [[] for _ in range(self.depth)]
        
        current_row = 0
        direction = 1  # 1 untuk turun, -1 untuk naik
        
        # Isi karakter ke dalam pola panah
        for char in text:
            rows[current_row].append(char)
            
            # Ubah arah di batas atas dan bawah
            if current_row == 0:
                direction = 1
            elif current_row == self.depth - 1:
                direction = -1
            
            current_row += direction
        
        # Gabungkan semua baris untuk mendapatkan ciphertext
        ciphertext = ''.join([''.join(row) for row in rows])
        
        return ciphertext, rows
    
    def decrypt_text(self, ciphertext):
        """
        Dekripsi teks dari pola panah
        """
        if len(ciphertext) <= 1:
            return ciphertext
        
        # Hitung jumlah karakter di setiap baris
        row_lengths = [0] * self.depth
        current_row = 0
        direction = 1
        
        for _ in range(len(ciphertext)):
            row_lengths[current_row] += 1
            
            if current_row == 0:
                direction = 1
            elif current_row == self.depth - 1:
                direction = -1
            
            current_row += direction
        
        # Bagi ciphertext ke dalam baris-baris
        rows = []
        start = 0
        for length in row_lengths:
            rows.append(list(ciphertext[start:start + length]))
            start += length
        
        # Rekonstruksi teks asli dengan mengikuti pola panah
        plaintext = []
        current_row = 0
        direction = 1
        row_indices = [0] * self.depth
        
        for _ in range(len(ciphertext)):
            plaintext.append(rows[current_row][row_indices[current_row]])
            row_indices[current_row] += 1
            
            if current_row == 0:
                direction = 1
            elif current_row == self.depth - 1:
                direction = -1
            
            current_row += direction
        
        return ''.join(plaintext)
    
    def visualize_pattern(self, text, rows):
        """
        Visualisasi pola panah untuk debugging
        """
        print(f"\nVisualisasi Pola Panah (Depth: {self.depth}):")
        print("=" * 50)
        
        # Buat grid untuk visualisasi
        grid = [[' ' for _ in range(len(text))] for _ in range(self.depth)]
        
        current_row = 0
        direction = 1
        col = 0
        
        for char in text.replace(" ", "").upper():
            grid[current_row][col] = char
            
            if current_row == 0:
                direction = 1
            elif current_row == self.depth - 1:
                direction = -1
            
            current_row += direction
            col += 1
        
        # Print grid
        for i, row in enumerate(grid):
            print(f"Baris {i+1}: {''.join(row[:col])}")
        
        print(f"\nHasil per baris:")
        for i, row in enumerate(rows):
            print(f"Baris {i+1}: {''.join(row)}")
    
    def encrypt_file(self, input_file, output_file):
        """
        Enkripsi file teks
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            encrypted, rows = self.encrypt_text(content)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(encrypted)
            
            print(f"File berhasil dienkripsi: {input_file} -> {output_file}")
            return encrypted, rows
            
        except FileNotFoundError:
            print(f"Error: File {input_file} tidak ditemukan!")
            return None, None
        except Exception as e:
            print(f"Error saat enkripsi: {e}")
            return None, None
    
    def decrypt_file(self, input_file, output_file):
        """
        Dekripsi file teks
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            decrypted = self.decrypt_text(content)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decrypted)
            
            print(f"File berhasil didekripsi: {input_file} -> {output_file}")
            return decrypted
            
        except FileNotFoundError:
            print(f"Error: File {input_file} tidak ditemukan!")
            return None
        except Exception as e:
            print(f"Error saat dekripsi: {e}")
            return None

def demo():
    """
    Demonstrasi penggunaan ArrowCipher
    """
    print("=== DEMO ENKRIPSI DEKRIPSI POLA PANAH ===")
    
    # Inisialisasi cipher dengan depth 4
    cipher = ArrowCipher(depth=4)
    
    # Contoh teks
    original_text = "HELLO WORLD CIPHER ARROW PATTERN"
    print(f"Teks asli: {original_text}")
    
    # Enkripsi
    encrypted, rows = cipher.encrypt_text(original_text)
    print(f"Teks terenkripsi: {encrypted}")
    
    # Visualisasi pola
    cipher.visualize_pattern(original_text, rows)
    
    # Dekripsi
    decrypted = cipher.decrypt_text(encrypted)
    print(f"Teks terdekripsi: {decrypted}")
    
    # Verifikasi
    original_clean = original_text.replace(" ", "").upper()
    print(f"\nVerifikasi:")
    print(f"Asli (tanpa spasi): {original_clean}")
    print(f"Hasil dekripsi: {decrypted}")
    print(f"Berhasil: {'✓' if original_clean == decrypted else '✗'}")
    
    print("\n" + "="*50)
    
    # Demo dengan file
    print("Demo Enkripsi/Dekripsi File:")
    
    # Buat file contoh
    sample_file = "sample.txt"
    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("Ini adalah contoh file yang akan dienkripsi menggunakan cipher pola panah")
    
    # Enkripsi file
    cipher.encrypt_file(sample_file, encrypted_file)
    
    # Dekripsi file
    cipher.decrypt_file(encrypted_file, decrypted_file)
    
    # Tampilkan isi file
    print(f"\nIsi file asli:")
    with open(sample_file, 'r', encoding='utf-8') as f:
        print(f"  {f.read()}")
    
    print(f"\nIsi file terenkripsi:")
    with open(encrypted_file, 'r', encoding='utf-8') as f:
        print(f"  {f.read()}")
    
    print(f"\nIsi file terdekripsi:")
    with open(decrypted_file, 'r', encoding='utf-8') as f:
        print(f"  {f.read()}")
    
    # Cleanup file demo
    for file in [sample_file, encrypted_file, decrypted_file]:
        if os.path.exists(file):
            os.remove(file)

def interactive_mode():
    """
    Mode interaktif untuk pengguna
    """
    print("\n=== MODE INTERAKTIF ===")
    
    while True:
        print("\nPilihan:")
        print("1. Enkripsi teks")
        print("2. Dekripsi teks")
        print("3. Enkripsi file")
        print("4. Dekripsi file")
        print("5. Keluar")
        
        choice = input("\nPilih opsi (1-5): ").strip()
        
        if choice == '1':
            text = input("Masukkan teks yang akan dienkripsi: ")
            depth = int(input("Masukkan kedalaman pola (default 4): ") or 4)
            cipher = ArrowCipher(depth)
            encrypted, rows = cipher.encrypt_text(text)
            print(f"Hasil enkripsi: {encrypted}")
            
            show_pattern = input("Tampilkan pola? (y/n): ").lower() == 'y'
            if show_pattern:
                cipher.visualize_pattern(text, rows)
        
        elif choice == '2':
            text = input("Masukkan teks yang akan didekripsi: ")
            depth = int(input("Masukkan kedalaman pola (default 4): ") or 4)
            cipher = ArrowCipher(depth)
            decrypted = cipher.decrypt_text(text)
            print(f"Hasil dekripsi: {decrypted}")
        
        elif choice == '3':
            input_file = input("Nama file input: ")
            output_file = input("Nama file output: ")
            depth = int(input("Masukkan kedalaman pola (default 4): ") or 4)
            cipher = ArrowCipher(depth)
            cipher.encrypt_file(input_file, output_file)
        
        elif choice == '4':
            input_file = input("Nama file input: ")
            output_file = input("Nama file output: ")
            depth = int(input("Masukkan kedalaman pola (default 4): ") or 4)
            cipher = ArrowCipher(depth)
            cipher.decrypt_file(input_file, output_file)
        
        elif choice == '5':
            print("Terima kasih!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    # Jalankan demo
    demo()
    
    # Jalankan mode interaktif
    interactive_mode()