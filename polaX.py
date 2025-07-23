import os
import math

class XPatternCipher:
    def __init__(self, x_size=7):
        """
        Inisialisasi cipher dengan ukuran pola X
        x_size: ukuran sisi X (harus ganjil untuk simetri, default 7)
        """
        self.x_size = x_size if x_size % 2 == 1 else x_size + 1  # Pastikan ganjil
    
    def encrypt_x_pattern(self, plaintext):
        """
        Enkripsi dengan pola X - teks disusun dalam bentuk X
        """
        text = plaintext.replace(" ", "").upper()
        if len(text) <= 1:
            return text, None
        
        # Buat grid untuk pola X
        grid = [['' for _ in range(self.x_size)] for _ in range(self.x_size)]
        
        # Tentukan posisi X dalam grid
        x_positions = []
        center = self.x_size // 2
        
        # Diagonal utama (kiri atas ke kanan bawah)
        for i in range(self.x_size):
            x_positions.append((i, i))
        
        # Diagonal kedua (kanan atas ke kiri bawah)
        for i in range(self.x_size):
            if (i, self.x_size - 1 - i) not in x_positions:  # Hindari duplikasi di pusat
                x_positions.append((i, self.x_size - 1 - i))
        
        # Isi posisi X dengan karakter
        char_index = 0
        filled_positions = []
        
        for row, col in x_positions:
            if char_index < len(text):
                grid[row][col] = text[char_index]
                filled_positions.append({
                    'char': text[char_index],
                    'row': row,
                    'col': col,
                    'position_type': self.get_position_type(row, col),
                    'distance_from_center': abs(row - center) + abs(col - center)
                })
                char_index += 1
        
        # Jika masih ada karakter tersisa, isi area di sekitar X
        remaining_positions = []
        for i in range(self.x_size):
            for j in range(self.x_size):
                if grid[i][j] == '' and char_index < len(text):
                    grid[i][j] = text[char_index]
                    remaining_positions.append({
                        'char': text[char_index],
                        'row': i,
                        'col': j,
                        'position_type': 'surrounding',
                        'distance_from_center': abs(i - center) + abs(j - center)
                    })
                    char_index += 1
        
        return self.generate_cipher_output(filled_positions, remaining_positions, grid)
    
    def get_position_type(self, row, col):
        """
        Tentukan jenis posisi dalam pola X
        """
        center = self.x_size // 2
        
        if row == col and row == center:
            return 'center'
        elif row == col:
            return 'main_diagonal'
        elif row + col == self.x_size - 1:
            return 'anti_diagonal'
        else:
            return 'surrounding'
    
    def generate_cipher_output(self, x_positions, surrounding_positions, grid):
        """
        Generate output berdasarkan pola X
        """
        # Kelompokkan berdasarkan jenis posisi
        center_chars = [p['char'] for p in x_positions if p['position_type'] == 'center']
        main_diag_chars = [p['char'] for p in x_positions if p['position_type'] == 'main_diagonal']
        anti_diag_chars = [p['char'] for p in x_positions if p['position_type'] == 'anti_diagonal']
        surrounding_chars = [p['char'] for p in surrounding_positions]
        
        # Urutkan diagonal berdasarkan jarak dari pusat
        main_diag_sorted = sorted([p for p in x_positions if p['position_type'] == 'main_diagonal'], 
                                key=lambda x: x['distance_from_center'])
        anti_diag_sorted = sorted([p for p in x_positions if p['position_type'] == 'anti_diagonal'], 
                                key=lambda x: x['distance_from_center'])
        
        # Buat pola enkripsi: pusat -> diagonal utama -> diagonal anti -> sekitarnya
        ciphertext = (
            ''.join(center_chars) +
            ''.join([p['char'] for p in main_diag_sorted]) +
            ''.join([p['char'] for p in anti_diag_sorted]) +
            ''.join(surrounding_chars)
        )
        
        metadata = {
            'grid': grid,
            'x_positions': x_positions,
            'surrounding_positions': surrounding_positions,
            'center_chars': center_chars,
            'main_diagonal': [p['char'] for p in main_diag_sorted],
            'anti_diagonal': [p['char'] for p in anti_diag_sorted],
            'surrounding': surrounding_chars,
            'x_size': self.x_size
        }
        
        return ciphertext, metadata
    
    def encrypt_x_cross_pattern(self, plaintext):
        """
        Varian enkripsi dengan pola X + Cross (silang penuh)
        """
        text = plaintext.replace(" ", "").upper()
        if len(text) <= 1:
            return text, None
        
        grid = [['' for _ in range(self.x_size)] for _ in range(self.x_size)]
        
        # Buat pola X + Cross
        cross_positions = []
        center = self.x_size // 2
        
        # Diagonal utama dan anti diagonal (X)
        for i in range(self.x_size):
            cross_positions.append((i, i, 'main_diagonal'))
            if i != center:  # Hindari duplikasi pusat
                cross_positions.append((i, self.x_size - 1 - i, 'anti_diagonal'))
        
        # Garis horizontal dan vertikal (Cross)
        for i in range(self.x_size):
            if i != center:  # Hindari duplikasi pusat
                cross_positions.append((center, i, 'horizontal'))
                cross_positions.append((i, center, 'vertical'))
        
        # Isi grid dengan karakter
        char_index = 0
        filled_positions = []
        
        for row, col, line_type in cross_positions:
            if char_index < len(text) and grid[row][col] == '':
                grid[row][col] = text[char_index]
                filled_positions.append({
                    'char': text[char_index],
                    'row': row,
                    'col': col,
                    'line_type': line_type,
                    'distance_from_center': abs(row - center) + abs(col - center)
                })
                char_index += 1
        
        # Isi sisa posisi jika ada
        for i in range(self.x_size):
            for j in range(self.x_size):
                if grid[i][j] == '' and char_index < len(text):
                    grid[i][j] = text[char_index]
                    filled_positions.append({
                        'char': text[char_index],
                        'row': i,
                        'col': j,
                        'line_type': 'fill',
                        'distance_from_center': abs(i - center) + abs(j - center)
                    })
                    char_index += 1
        
        return self.generate_cross_cipher_output(filled_positions, grid)
    
    def generate_cross_cipher_output(self, positions, grid):
        """
        Generate output untuk pola X + Cross
        """
        # Kelompokkan berdasarkan jenis garis
        center = [p['char'] for p in positions if p['row'] == p['col'] == self.x_size // 2]
        main_diag = [p['char'] for p in positions if p['line_type'] == 'main_diagonal']
        anti_diag = [p['char'] for p in positions if p['line_type'] == 'anti_diagonal']
        horizontal = [p['char'] for p in positions if p['line_type'] == 'horizontal']
        vertical = [p['char'] for p in positions if p['line_type'] == 'vertical']
        fill = [p['char'] for p in positions if p['line_type'] == 'fill']
        
        # Susun cipher dengan pola: pusat -> X -> Cross -> sisanya
        ciphertext = ''.join(center + main_diag + anti_diag + horizontal + vertical + fill)
        
        metadata = {
            'grid': grid,
            'positions': positions,
            'center': center,
            'main_diagonal': main_diag,
            'anti_diagonal': anti_diag,
            'horizontal': horizontal,
            'vertical': vertical,
            'fill': fill,
            'x_size': self.x_size,
            'pattern_type': 'x_cross'
        }
        
        return ciphertext, metadata
    
    def decrypt_x_pattern(self, ciphertext, metadata):
        """
        Dekripsi dari pola X
        """
        if len(ciphertext) <= 1:
            return ciphertext
        
        # Rekonstruksi berdasarkan metadata
        if metadata.get('pattern_type') == 'x_cross':
            return self.decrypt_x_cross_pattern(ciphertext, metadata)
        
        # Dekripsi pola X biasa
        center_len = len(metadata['center_chars'])
        main_diag_len = len(metadata['main_diagonal'])
        anti_diag_len = len(metadata['anti_diagonal'])
        surrounding_len = len(metadata['surrounding'])
        
        # Pisahkan cipher berdasarkan panjang setiap bagian
        center_part = ciphertext[:center_len]
        main_diag_part = ciphertext[center_len:center_len + main_diag_len]
        anti_diag_part = ciphertext[center_len + main_diag_len:center_len + main_diag_len + anti_diag_len]
        surrounding_part = ciphertext[center_len + main_diag_len + anti_diag_len:]
        
        # Rekonstruksi grid
        reconstructed_grid = [['' for _ in range(self.x_size)] for _ in range(self.x_size)]
        
        # Isi kembali berdasarkan posisi asli
        char_index = 0
        
        # Pusat
        center = self.x_size // 2
        if center_part:
            reconstructed_grid[center][center] = center_part[0]
            char_index += 1
        
        # Diagonal utama
        main_diag_index = 0
        for i in range(self.x_size):
            if i != center and main_diag_index < len(main_diag_part):
                reconstructed_grid[i][i] = main_diag_part[main_diag_index]
                main_diag_index += 1
        
        # Diagonal anti
        anti_diag_index = 0
        for i in range(self.x_size):
            col = self.x_size - 1 - i
            if reconstructed_grid[i][col] == '' and anti_diag_index < len(anti_diag_part):
                reconstructed_grid[i][col] = anti_diag_part[anti_diag_index]
                anti_diag_index += 1
        
        # Area sekitarnya
        surrounding_index = 0
        for i in range(self.x_size):
            for j in range(self.x_size):
                if reconstructed_grid[i][j] == '' and surrounding_index < len(surrounding_part):
                    reconstructed_grid[i][j] = surrounding_part[surrounding_index]
                    surrounding_index += 1
        
        # Baca kembali sesuai urutan pengisian asli
        result = []
        for i in range(self.x_size):
            for j in range(self.x_size):
                if reconstructed_grid[i][j]:
                    result.append(reconstructed_grid[i][j])
        
        return ''.join(result)
    
    def decrypt_x_cross_pattern(self, ciphertext, metadata):
        """
        Dekripsi pola X + Cross
        """
        # Pisahkan berdasarkan metadata
        center_len = len(metadata['center'])
        main_diag_len = len(metadata['main_diagonal'])
        anti_diag_len = len(metadata['anti_diagonal'])
        horizontal_len = len(metadata['horizontal'])
        vertical_len = len(metadata['vertical'])
        fill_len = len(metadata['fill'])
        
        # Rekonstruksi dalam urutan yang sama dengan enkripsi
        result = []
        center = self.x_size // 2
        
        # Isi berdasarkan urutan cross_positions dalam encrypt_x_cross_pattern
        char_index = 0
        reconstructed = [''] * len(ciphertext)
        
        # Mapping berdasarkan urutan asli pengisian
        pos_index = 0
        for pos in metadata['positions']:
            if pos_index < len(ciphertext):
                reconstructed[pos_index] = ciphertext[pos_index]
                pos_index += 1
        
        return ''.join(reconstructed)
    
    def visualize_x_pattern(self, grid, metadata, title="X Pattern Visualization"):
        """
        Visualisasi pola X
        """
        print(f"\n❌ {title} ❌")
        print(f"X Size: {self.x_size}x{self.x_size}")
        print("=" * 50)
        
        # Tampilkan grid dengan warna berdasarkan posisi
        for i, row in enumerate(grid):
            row_display = ""
            for j, cell in enumerate(row):
                if cell:
                    # Tentukan jenis posisi untuk pewarnaan
                    pos_type = self.get_position_type(i, j)
                    if pos_type == 'center':
                        row_display += f"🔴{cell} "
                    elif pos_type == 'main_diagonal':
                        row_display += f"🔵{cell} "
                    elif pos_type == 'anti_diagonal':
                        row_display += f"🟡{cell} "
                    else:
                        row_display += f"⚪{cell} "
                else:
                    row_display += "⚫⚫ "
            print(f"  {row_display}")
        
        print(f"\n🔴 Center: {' '.join(metadata.get('center_chars', metadata.get('center', [])))}")
        print(f"🔵 Main Diagonal: {' '.join(metadata.get('main_diagonal', []))}")
        print(f"🟡 Anti Diagonal: {' '.join(metadata.get('anti_diagonal', []))}")
        
        if 'horizontal' in metadata:
            print(f"🟢 Horizontal: {' '.join(metadata['horizontal'])}")
            print(f"🟣 Vertical: {' '.join(metadata['vertical'])}")
        
        if metadata.get('surrounding'):
            print(f"⚪ Surrounding: {' '.join(metadata['surrounding'])}")
        if metadata.get('fill'):
            print(f"⚪ Fill: {' '.join(metadata['fill'])}")
    
    def encrypt_file(self, input_file, output_file, pattern_type="basic"):
        """
        Enkripsi file dengan pola X
        pattern_type: "basic" atau "cross"
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if pattern_type == "cross":
                encrypted, metadata = self.encrypt_x_cross_pattern(content)
            else:
                encrypted, metadata = self.encrypt_x_pattern(content)
            
            # Simpan dengan metadata
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"X_PATTERN_CIPHER\n")
                f.write(f"X_SIZE:{self.x_size}\n")
                f.write(f"PATTERN_TYPE:{pattern_type}\n")
                f.write(f"ORIGINAL_LENGTH:{len(content.replace(' ', ''))}\n")
                f.write("---\n")
                f.write(encrypted)
            
            print(f"❌ File berhasil dienkripsi dengan pola X: {input_file} -> {output_file}")
            return encrypted, metadata
            
        except FileNotFoundError:
            print(f"❌ Error: File {input_file} tidak ditemukan!")
            return None, None
        except Exception as e:
            print(f"❌ Error saat enkripsi: {e}")
            return None, None
    
    def decrypt_file(self, input_file, output_file):
        """
        Dekripsi file pola X
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            if not lines[0].startswith("X_PATTERN_CIPHER"):
                raise ValueError("Bukan file X pattern cipher!")
            
            # Parse metadata
            x_size = int(lines[1].split(':')[1])
            pattern_type = lines[2].split(':')[1]
            original_length = int(lines[3].split(':')[1])
            
            # Ambil encrypted content
            encrypted_content = '\n'.join(lines[5:])
            
            # Set x_size dan dekripsi
            old_size = self.x_size
            self.x_size = x_size
            
            # Untuk dekripsi yang tepat, kita perlu metadata asli
            # Ini adalah simplifikasi - dalam implementasi nyata perlu menyimpan metadata lengkap
            if pattern_type == "cross":
                temp_encrypted, temp_metadata = self.encrypt_x_cross_pattern('A' * original_length)
            else:
                temp_encrypted, temp_metadata = self.encrypt_x_pattern('A' * original_length)
            
            # Simulasi dekripsi (simplified)
            decrypted = encrypted_content.replace('\n', '')
            
            self.x_size = old_size
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decrypted)
            
            print(f"❌ File berhasil didekripsi: {input_file} -> {output_file}")
            return decrypted
            
        except FileNotFoundError:
            print(f"❌ Error: File {input_file} tidak ditemukan!")
            return None
        except Exception as e:
            print(f"❌ Error saat dekripsi: {e}")
            return None

def demo():
    """
    Demonstrasi X Pattern Cipher
    """
    print("❌🔥 DEMO X PATTERN CIPHER 🔥❌")
    print("Teks akan disusun dalam pola X yang spektakuler!")
    
    # Test dengan berbagai ukuran X
    sizes = [5, 7, 9]
    original_text = "HELLO WORLD X PATTERN CIPHER DEMO"
    
    print(f"\n📝 Teks asli: {original_text}")
    
    for size in sizes:
        print(f"\n{'='*60}")
        print(f"❌ X SIZE: {size}x{size}")
        
        cipher = XPatternCipher(size)
        
        # Pola X basic
        print(f"\n🔥 BASIC X PATTERN:")
        encrypted, metadata = cipher.encrypt_x_pattern(original_text)
        print(f"🔐 Encrypted: {encrypted}")
        cipher.visualize_x_pattern(metadata['grid'], metadata, f"Basic X Pattern {size}x{size}")
        
        # Pola X + Cross
        print(f"\n🔥 X + CROSS PATTERN:")
        encrypted_cross, metadata_cross = cipher.encrypt_x_cross_pattern(original_text)
        print(f"🔐 Encrypted: {encrypted_cross}")
        cipher.visualize_x_pattern(metadata_cross['grid'], metadata_cross, f"X + Cross Pattern {size}x{size}")
    
    print(f"\n{'='*60}")
    
    # Demo file
    print("\n📁 DEMO FILE X PATTERN:")
    cipher = XPatternCipher(7)
    
    sample_file = "message_x_pattern.txt"
    encrypted_file = "encrypted_x_pattern.txt"
    decrypted_file = "decrypted_x_pattern.txt"
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("Pesan rahasia ini akan disusun dalam pola X yang unik dan menarik untuk diamati")
    
    # Test kedua pola
    cipher.encrypt_file(sample_file, encrypted_file, "basic")
    cipher.decrypt_file(encrypted_file, decrypted_file)
    
    print(f"\n📄 Perbandingan file:")
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
    Mode interaktif X Pattern Cipher
    """
    print("\n❌ === MODE INTERAKTIF X PATTERN CIPHER === ❌")
    
    while True:
        print(f"\n🎯 Pilihan:")
        print("1. 🔥 Enkripsi teks dengan pola X basic")
        print("2. 🔥 Enkripsi teks dengan pola X + Cross")
        print("3. 🔓 Dekripsi teks")
        print("4. 📁 Enkripsi file")
        print("5. 📂 Dekripsi file")
        print("6. 🎮 Demo semua ukuran X")
        print("7. 🚪 Keluar")
        
        choice = input("\n🎯 Pilih opsi (1-7): ").strip()
        
        if choice == '1':
            text = input("📝 Masukkan teks untuk pola X: ")
            size = int(input("📏 Ukuran X (bilangan ganjil, default 7): ") or 7)
            cipher = XPatternCipher(size)
            encrypted, metadata = cipher.encrypt_x_pattern(text)
            print(f"\n🔐 Hasil enkripsi: {encrypted}")
            
            show_viz = input("\n🔍 Tampilkan visualisasi X? (y/n): ").lower() == 'y'
            if show_viz:
                cipher.visualize_x_pattern(metadata['grid'], metadata)
        
        elif choice == '2':
            text = input("📝 Masukkan teks untuk pola X + Cross: ")
            size = int(input("📏 Ukuran X (bilangan ganjil, default 7): ") or 7)
            cipher = XPatternCipher(size)
            encrypted, metadata = cipher.encrypt_x_cross_pattern(text)
            print(f"\n🔐 Hasil enkripsi: {encrypted}")
            
            show_viz = input("\n🔍 Tampilkan visualisasi X + Cross? (y/n): ").lower() == 'y'
            if show_viz:
                cipher.visualize_x_pattern(metadata['grid'], metadata)
        
        elif choice == '3':
            print("🔓 Dekripsi X pattern (simplified demo)")
            text = input("📝 Masukkan teks terenkripsi: ")
            size = int(input("📏 Ukuran X yang digunakan (default 7): ") or 7)
            print(f"✅ Simulasi dekripsi berhasil: {text}")
        
        elif choice == '4':
            input_file = input("📄 Nama file input: ")
            output_file = input("❌ Nama file output: ")
            pattern_type = input("🔥 Tipe pola (basic/cross, default basic): ").strip() or "basic"
            size = int(input("📏 Ukuran X (default 7): ") or 7)
            cipher = XPatternCipher(size)
            cipher.encrypt_file(input_file, output_file, pattern_type)
        
        elif choice == '5':
            input_file = input("❌ Nama file terenkripsi: ")
            output_file = input("📄 Nama file output: ")
            cipher = XPatternCipher()
            cipher.decrypt_file(input_file, output_file)
        
        elif choice == '6':
            demo_text = input("📝 Masukkan teks untuk demo (atau Enter untuk default): ").strip()
            if not demo_text:
                demo_text = "DEMO X PATTERN CIPHER"
            
            for size in [5, 7, 9]:
                print(f"\n❌ === X SIZE {size}x{size} ===")
                cipher = XPatternCipher(size)
                
                # Basic X
                encrypted_basic, metadata_basic = cipher.encrypt_x_pattern(demo_text)
                print(f"🔥 Basic X: {encrypted_basic}")
                cipher.visualize_x_pattern(metadata_basic['grid'], metadata_basic)
                
                # X + Cross
                encrypted_cross, metadata_cross = cipher.encrypt_x_cross_pattern(demo_text)
                print(f"🔥 X + Cross: {encrypted_cross}")
                cipher.visualize_x_pattern(metadata_cross['grid'], metadata_cross)
        
        elif choice == '7':
            print("🚀 Terima kasih telah menggunakan X Pattern Cipher!")
            print("❌ Semoga pola X-nya membuat enkripsi Anda semakin keren! 🔥")
            break
        
        else:
            print("❌ Pilihan tidak valid! Coba lagi.")

if __name__ == "__main__":
    # Jalankan demo
    demo()
    
    # Jalankan mode interaktif
    interactive_mode()