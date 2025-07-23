import os

class StaircaseCipher:
    def __init__(self, step_size=3):
        """
        Inisialisasi cipher dengan ukuran langkah tangga
        step_size: jumlah karakter per langkah tangga (default 3)
        """
        self.step_size = step_size
    
    def encrypt_text(self, plaintext):
        """
        Enkripsi teks menggunakan pola tangga
        """
        if len(plaintext) <= 1:
            return plaintext
        
        # Hilangkan spasi dan ubah ke uppercase
        text = plaintext.replace(" ", "").upper()
        
        # Buat struktur tangga
        stairs = []
        current_pos = 0
        stair_level = 0
        
        while current_pos < len(text):
            # Hitung jumlah karakter untuk level tangga ini
            chars_in_level = min(self.step_size + stair_level, len(text) - current_pos)
            
            # Ambil karakter untuk level ini
            level_chars = text[current_pos:current_pos + chars_in_level]
            stairs.append(level_chars)
            
            current_pos += chars_in_level
            stair_level += 1
        
        # Gabungkan semua level untuk mendapatkan ciphertext
        ciphertext = ''.join(stairs)
        
        return ciphertext, stairs
    
    def decrypt_text(self, ciphertext):
        """
        Dekripsi teks dari pola tangga
        """
        if len(ciphertext) <= 1:
            return ciphertext
        
        # Rekonstruksi struktur tangga
        stairs = []
        current_pos = 0
        stair_level = 0
        
        while current_pos < len(ciphertext):
            # Hitung jumlah karakter untuk level tangga ini
            chars_in_level = min(self.step_size + stair_level, len(ciphertext) - current_pos)
            
            # Ambil karakter untuk level ini
            level_chars = ciphertext[current_pos:current_pos + chars_in_level]
            stairs.append(level_chars)
            
            current_pos += chars_in_level
            stair_level += 1
        
        # Gabungkan kembali untuk mendapatkan plaintext
        plaintext = ''.join(stairs)
        
        return plaintext
    
    def encrypt_text_column_read(self, plaintext):
        """
        Enkripsi dengan pola tangga dan pembacaan kolom
        (Varian yang lebih kompleks)
        """
        if len(plaintext) <= 1:
            return plaintext
        
        # Hilangkan spasi dan ubah ke uppercase
        text = plaintext.replace(" ", "").upper()
        
        # Buat grid tangga
        max_width = self.step_size + (len(text) // self.step_size)
        grid = [[' ' for _ in range(max_width)] for _ in range(max_width)]
        
        # Isi grid dengan pola tangga
        char_index = 0
        row = 0
        
        while char_index < len(text) and row < max_width:
            # Jumlah karakter untuk baris ini
            chars_in_row = min(self.step_size + row, len(text) - char_index, max_width - row)
            
            # Isi baris mulai dari kolom = row
            for col in range(row, row + chars_in_row):
                if char_index < len(text) and col < max_width:
                    grid[row][col] = text[char_index]
                    char_index += 1
            
            row += 1
        
        # Baca kolom demi kolom untuk enkripsi
        ciphertext = ""
        for col in range(max_width):
            for row in range(max_width):
                if grid[row][col] != ' ':
                    ciphertext += grid[row][col]
        
        return ciphertext, grid
    
    def decrypt_text_column_read(self, ciphertext, original_length):
        """
        Dekripsi dari pola tangga dengan pembacaan kolom
        """
        if len(ciphertext) <= 1:
            return ciphertext
        
        # Tentukan ukuran grid
        max_width = self.step_size + (original_length // self.step_size) + 1
        grid = [[' ' for _ in range(max_width)] for _ in range(max_width)]
        
        # Tentukan posisi yang valid dalam pola tangga
        valid_positions = []
        row = 0
        char_count = 0
        
        while char_count < original_length and row < max_width:
            chars_in_row = min(self.step_size + row, original_length - char_count, max_width - row)
            
            for col in range(row, row + chars_in_row):
                if col < max_width:
                    valid_positions.append((row, col))
                    char_count += 1
            
            row += 1
        
        # Isi grid berdasarkan urutan kolom
        cipher_index = 0
        for col in range(max_width):
            for row in range(max_width):
                if (row, col) in valid_positions and cipher_index < len(ciphertext):
                    grid[row][col] = ciphertext[cipher_index]
                    cipher_index += 1
        
        # Baca kembali sesuai pola tangga
        plaintext = ""
        for row in range(max_width):
            for col in range(row, max_width):
                if grid[row][col] != ' ':
                    plaintext += grid[row][col]
        
        return plaintext
    
    def visualize_staircase_pattern(self, text, stairs):
        """
        Visualisasi pola tangga
        """
        print(f"\nVisualisasi Pola Tangga (Step Size: {self.step_size}):")
        print("=" * 60)
        
        max_length = max(len(stair) for stair in stairs) if stairs else 0
        
        for i, stair in enumerate(stairs):
            indent = " " * (i * 2)  # Indentasi untuk efek tangga
            print(f"Level {i+1}: {indent}{stair}")
        
        print(f"\nDetail per level:")
        for i, stair in enumerate(stairs):
            print(f"Level {i+1}: {len(stair)} karakter - '{stair}'")
    
    def visualize_grid_pattern(self, grid, title="Grid Pattern"):
        """
        Visualisasi pola grid
        """
        print(f"\n{title}:")
        print("=" * 40)
        
        for i, row in enumerate(grid):
            row_str = ""
            for cell in row:
                row_str += cell if cell != ' ' else '.'
            if any(cell != ' ' for cell in row):  # Hanya tampilkan baris yang tidak kosong
                print(f"Baris {i+1}: {row_str}")
    
    def encrypt_file(self, input_file, output_file, method="simple"):
        """
        Enkripsi file teks
        method: "simple" atau "column" untuk metode yang berbeda
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if method == "simple":
                encrypted, stairs = self.encrypt_text(content)
                metadata = f"METHOD:simple\nSTEP_SIZE:{self.step_size}\nORIGINAL_LENGTH:{len(content.replace(' ', ''))}\n---\n"
            else:
                encrypted, grid = self.encrypt_text_column_read(content)
                metadata = f"METHOD:column\nSTEP_SIZE:{self.step_size}\nORIGINAL_LENGTH:{len(content.replace(' ', ''))}\n---\n"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(metadata + encrypted)
            
            print(f"File berhasil dienkripsi: {input_file} -> {output_file}")
            return encrypted
            
        except FileNotFoundError:
            print(f"Error: File {input_file} tidak ditemukan!")
            return None
        except Exception as e:
            print(f"Error saat enkripsi: {e}")
            return None
    
    def decrypt_file(self, input_file, output_file):
        """
        Dekripsi file teks
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse metadata
            parts = content.split('---\n', 1)
            if len(parts) != 2:
                raise ValueError("Format file tidak valid")
            
            metadata_lines = parts[0].strip().split('\n')
            encrypted_content = parts[1]
            
            # Extract metadata
            method = "simple"
            original_length = len(encrypted_content)
            
            for line in metadata_lines:
                if line.startswith("METHOD:"):
                    method = line.split(":")[1]
                elif line.startswith("STEP_SIZE:"):
                    self.step_size = int(line.split(":")[1])
                elif line.startswith("ORIGINAL_LENGTH:"):
                    original_length = int(line.split(":")[1])
            
            # Dekripsi sesuai metode
            if method == "simple":
                decrypted = self.decrypt_text(encrypted_content)
            else:
                decrypted = self.decrypt_text_column_read(encrypted_content, original_length)
            
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
    Demonstrasi penggunaan StaircaseCipher
    """
    print("=== DEMO ENKRIPSI DEKRIPSI POLA TANGGA ===")
    
    # Demo metode sederhana
    print("\n1. METODE TANGGA SEDERHANA:")
    cipher = StaircaseCipher(step_size=3)
    
    original_text = "HELLO WORLD STAIRCASE CIPHER"
    print(f"Teks asli: {original_text}")
    
    # Enkripsi sederhana
    encrypted, stairs = cipher.encrypt_text(original_text)
    print(f"Teks terenkripsi: {encrypted}")
    
    # Visualisasi
    cipher.visualize_staircase_pattern(original_text, stairs)
    
    # Dekripsi
    decrypted = cipher.decrypt_text(encrypted)
    print(f"Teks terdekripsi: {decrypted}")
    
    # Verifikasi
    original_clean = original_text.replace(" ", "").upper()
    print(f"\nVerifikasi:")
    print(f"Asli (tanpa spasi): {original_clean}")
    print(f"Hasil dekripsi: {decrypted}")
    print(f"Berhasil: {'✓' if original_clean == decrypted else '✗'}")
    
    print("\n" + "="*60)
    
    # Demo metode kolom
    print("\n2. METODE TANGGA + PEMBACAAN KOLOM:")
    
    encrypted_col, grid = cipher.encrypt_text_column_read(original_text)
    print(f"Teks terenkripsi (kolom): {encrypted_col}")
    
    cipher.visualize_grid_pattern(grid, "Grid Pola Tangga")
    
    decrypted_col = cipher.decrypt_text_column_read(encrypted_col, len(original_clean))
    print(f"Teks terdekripsi (kolom): {decrypted_col}")
    print(f"Berhasil: {'✓' if original_clean == decrypted_col else '✗'}")
    
    print("\n" + "="*60)
    
    # Demo dengan file
    print("\n3. DEMO FILE:")
    sample_file = "sample_stair.txt"
    encrypted_file = "encrypted_stair.txt"
    decrypted_file = "decrypted_stair.txt"
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("Ini adalah contoh enkripsi menggunakan pola tangga yang sangat menarik")
    
    # Test kedua metode
    cipher.encrypt_file(sample_file, encrypted_file, method="simple")
    cipher.decrypt_file(encrypted_file, decrypted_file)
    
    print(f"\nPerbandingan file:")
    with open(sample_file, 'r', encoding='utf-8') as f:
        print(f"Original: {f.read()}")
    with open(decrypted_file, 'r', encoding='utf-8') as f:
        print(f"Decrypted: {f.read()}")
    
    # Cleanup
    for file in [sample_file, encrypted_file, decrypted_file]:
        if os.path.exists(file):
            os.remove(file)

def interactive_mode():
    """
    Mode interaktif untuk pengguna
    """
    print("\n=== MODE INTERAKTIF POLA TANGGA ===")
    
    while True:
        print("\nPilihan:")
        print("1. Enkripsi teks (metode sederhana)")
        print("2. Dekripsi teks (metode sederhana)")
        print("3. Enkripsi teks (metode kolom)")
        print("4. Dekripsi teks (metode kolom)")
        print("5. Enkripsi file")
        print("6. Dekripsi file")
        print("7. Keluar")
        
        choice = input("\nPilih opsi (1-7): ").strip()
        
        if choice == '1':
            text = input("Masukkan teks yang akan dienkripsi: ")
            step_size = int(input("Masukkan ukuran langkah tangga (default 3): ") or 3)
            cipher = StaircaseCipher(step_size)
            encrypted, stairs = cipher.encrypt_text(text)
            print(f"Hasil enkripsi: {encrypted}")
            
            show_pattern = input("Tampilkan pola tangga? (y/n): ").lower() == 'y'
            if show_pattern:
                cipher.visualize_staircase_pattern(text, stairs)
        
        elif choice == '2':
            text = input("Masukkan teks yang akan didekripsi: ")
            step_size = int(input("Masukkan ukuran langkah tangga (default 3): ") or 3)
            cipher = StaircaseCipher(step_size)
            decrypted = cipher.decrypt_text(text)
            print(f"Hasil dekripsi: {decrypted}")
        
        elif choice == '3':
            text = input("Masukkan teks yang akan dienkripsi: ")
            step_size = int(input("Masukkan ukuran langkah tangga (default 3): ") or 3)
            cipher = StaircaseCipher(step_size)
            encrypted, grid = cipher.encrypt_text_column_read(text)
            print(f"Hasil enkripsi: {encrypted}")
            
            show_pattern = input("Tampilkan grid pattern? (y/n): ").lower() == 'y'
            if show_pattern:
                cipher.visualize_grid_pattern(grid)
        
        elif choice == '4':
            text = input("Masukkan teks yang akan didekripsi: ")
            original_length = int(input("Masukkan panjang teks asli: "))
            step_size = int(input("Masukkan ukuran langkah tangga (default 3): ") or 3)
            cipher = StaircaseCipher(step_size)
            decrypted = cipher.decrypt_text_column_read(text, original_length)
            print(f"Hasil dekripsi: {decrypted}")
        
        elif choice == '5':
            input_file = input("Nama file input: ")
            output_file = input("Nama file output: ")
            method = input("Metode (simple/column, default simple): ").strip() or "simple"
            step_size = int(input("Masukkan ukuran langkah tangga (default 3): ") or 3)
            cipher = StaircaseCipher(step_size)
            cipher.encrypt_file(input_file, output_file, method)
        
        elif choice == '6':
            input_file = input("Nama file input: ")
            output_file = input("Nama file output: ")
            cipher = StaircaseCipher()  # step_size akan dibaca dari metadata
            cipher.decrypt_file(input_file, output_file)
        
        elif choice == '7':
            print("Terima kasih!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    # Jalankan demo
    demo()
    
    # Jalankan mode interaktif
    interactive_mode()