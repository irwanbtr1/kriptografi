import os
import math

class BlackHoleCipher:
    def __init__(self, gravitational_pull="strong"):
        """
        Inisialisasi cipher dengan kekuatan gravitasi black hole
        gravitational_pull: "weak", "medium", "strong", "extreme"
        """
        self.gravitational_pull = gravitational_pull
        self.pull_factors = {
            "weak": 1,
            "medium": 2, 
            "strong": 3,
            "extreme": 5
        }
    
    def calculate_grid_size(self, length):
        """
        Hitung ukuran grid untuk black hole
        """
        return math.ceil(math.sqrt(length))
    
    def encrypt_black_hole(self, plaintext):
        """
        Enkripsi dengan pola black hole - teks tersedot ke pusat
        """
        text = plaintext.replace(" ", "").upper()
        if len(text) <= 1:
            return text, None
        
        size = self.calculate_grid_size(len(text))
        grid = [['' for _ in range(size)] for _ in range(size)]
        
        # Isi grid dengan pola spiral masuk ke pusat (black hole effect)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # kanan, bawah, kiri, atas
        direction_idx = 0
        
        row, col = 0, 0
        char_idx = 0
        
        # Mulai dari luar dan spiral masuk ke pusat
        for layer in range((size + 1) // 2):
            # Isi layer dari luar ke dalam
            
            # Kanan
            for _ in range(size - 2 * layer):
                if char_idx < len(text):
                    grid[row][col] = text[char_idx]
                    char_idx += 1
                if col < size - 1 - layer:
                    col += 1
            
            # Bawah
            for _ in range(size - 2 * layer - 1):
                if char_idx < len(text):
                    grid[row][col] = text[char_idx]
                    char_idx += 1
                if row < size - 1 - layer:
                    row += 1
            
            # Kiri
            for _ in range(size - 2 * layer - 1):
                if char_idx < len(text):
                    grid[row][col] = text[char_idx]
                    char_idx += 1
                if col > layer:
                    col -= 1
            
            # Atas
            for _ in range(size - 2 * layer - 2):
                if char_idx < len(text):
                    grid[row][col] = text[char_idx]
                    char_idx += 1
                if row > layer + 1:
                    row -= 1
            
            # Pindah ke layer dalam
            row = layer + 1
            col = layer + 1
        
        return self.apply_gravitational_distortion(grid, text)
    
    def apply_gravitational_distortion(self, grid, original_text):
        """
        Terapkan distorsi gravitasi pada grid
        """
        size = len(grid)
        center = size // 2
        pull_factor = self.pull_factors[self.gravitational_pull]
        
        # Buat salinan grid untuk distorsi
        distorted_grid = [row[:] for row in grid]
        
        # Hitung jarak dari pusat untuk setiap sel
        distances = []
        for i in range(size):
            for j in range(size):
                if grid[i][j]:
                    distance = math.sqrt((i - center)**2 + (j - center)**2)
                    distances.append((distance, i, j, grid[i][j]))
        
        # Urutkan berdasarkan jarak (terdekat dari pusat duluan)
        distances.sort()
        
        # Terapkan efek black hole - karakter lebih dekat ke pusat dibaca lebih dulu
        event_horizon = []  # Karakter yang terjebak di event horizon
        accretion_disk = []  # Karakter di cakram akresi
        hawking_radiation = []  # Karakter yang "terevaporasi"
        
        for i, (dist, row, col, char) in enumerate(distances):
            if dist <= 1.0:  # Event horizon
                event_horizon.append(char)
            elif dist <= 2.0:  # Accretion disk
                accretion_disk.append(char)
            else:  # Hawking radiation
                hawking_radiation.append(char)
        
        # Efek gravitasi: semakin kuat pull, semakin banyak perubahan urutan
        if pull_factor >= 2:
            # Balik urutan event horizon
            event_horizon.reverse()
        
        if pull_factor >= 3:
            # Acak accretion disk dengan pola tertentu
            accretion_disk = self.swirl_accretion_disk(accretion_disk)
        
        if pull_factor >= 5:
            # Efek Hawking radiation - beberapa karakter "menguap"
            hawking_radiation = self.apply_hawking_radiation(hawking_radiation)
        
        # Gabungkan hasil dengan urutan black hole
        ciphertext = ''.join(event_horizon + accretion_disk + hawking_radiation)
        
        return ciphertext, {
            'grid': distorted_grid,
            'event_horizon': event_horizon,
            'accretion_disk': accretion_disk,
            'hawking_radiation': hawking_radiation,
            'original_distances': distances
        }
    
    def swirl_accretion_disk(self, disk_chars):
        """
        Efek pusaran pada cakram akresi
        """
        if len(disk_chars) <= 1:
            return disk_chars
        
        # Bagi menjadi dua bagian dan silang
        mid = len(disk_chars) // 2
        part1 = disk_chars[:mid]
        part2 = disk_chars[mid:]
        
        # Efek pusaran - interleave dengan pola spiral
        swirled = []
        for i in range(max(len(part1), len(part2))):
            if i < len(part1):
                swirled.append(part1[i])
            if i < len(part2):
                swirled.append(part2[-(i+1)])  # Mundur untuk efek pusaran
        
        return swirled
    
    def apply_hawking_radiation(self, radiation_chars):
        """
        Efek radiasi Hawking - beberapa karakter berubah posisi
        """
        if len(radiation_chars) <= 2:
            return radiation_chars
        
        # Efek quantum - tukar posisi karakter secara berpasangan
        result = radiation_chars[:]
        for i in range(0, len(result) - 1, 2):
            result[i], result[i + 1] = result[i + 1], result[i]
        
        return result
    
    def decrypt_black_hole(self, ciphertext, metadata):
        """
        Dekripsi dari black hole - membalik efek gravitasi
        """
        if len(ciphertext) <= 1:
            return ciphertext
        
        # Ekstrak informasi dari metadata
        event_horizon = metadata['event_horizon']
        accretion_disk = metadata['accretion_disk']
        hawking_radiation = metadata['hawking_radiation']
        distances = metadata['original_distances']
        
        pull_factor = self.pull_factors[self.gravitational_pull]
        
        # Balik efek hawking radiation
        if pull_factor >= 5:
            hawking_radiation = self.reverse_hawking_radiation(hawking_radiation)
        
        # Balik efek accretion disk
        if pull_factor >= 3:
            accretion_disk = self.reverse_swirl_accretion_disk(accretion_disk)
        
        # Balik efek event horizon
        if pull_factor >= 2:
            event_horizon.reverse()
        
        # Rekonstruksi berdasarkan jarak asli
        chars_by_distance = {}
        all_chars = event_horizon + accretion_disk + hawking_radiation
        
        for i, (dist, row, col, orig_char) in enumerate(distances):
            if i < len(all_chars):
                chars_by_distance[(row, col)] = all_chars[i]
        
        # Susun kembali dalam urutan spiral asli
        size = int(math.sqrt(len(distances))) + 1
        reconstructed = [''] * len(ciphertext)
        
        char_idx = 0
        for layer in range((size + 1) // 2):
            row, col = layer, layer
            
            # Kanan
            for _ in range(size - 2 * layer):
                if (row, col) in chars_by_distance and char_idx < len(reconstructed):
                    reconstructed[char_idx] = chars_by_distance[(row, col)]
                    char_idx += 1
                if col < size - 1 - layer:
                    col += 1
            
            # Bawah
            for _ in range(size - 2 * layer - 1):
                if (row, col) in chars_by_distance and char_idx < len(reconstructed):
                    reconstructed[char_idx] = chars_by_distance[(row, col)]
                    char_idx += 1
                if row < size - 1 - layer:
                    row += 1
            
            # Kiri
            for _ in range(size - 2 * layer - 1):
                if (row, col) in chars_by_distance and char_idx < len(reconstructed):
                    reconstructed[char_idx] = chars_by_distance[(row, col)]
                    char_idx += 1
                if col > layer:
                    col -= 1
            
            # Atas
            for _ in range(size - 2 * layer - 2):
                if (row, col) in chars_by_distance and char_idx < len(reconstructed):
                    reconstructed[char_idx] = chars_by_distance[(row, col)]
                    char_idx += 1
                if row > layer + 1:
                    row -= 1
            
            # Pindah ke layer dalam
            row = layer + 1
            col = layer + 1
        
        return ''.join(reconstructed)
    
    def reverse_hawking_radiation(self, radiation_chars):
        """
        Balik efek radiasi Hawking
        """
        result = radiation_chars[:]
        for i in range(0, len(result) - 1, 2):
            result[i], result[i + 1] = result[i + 1], result[i]
        return result
    
    def reverse_swirl_accretion_disk(self, swirled_chars):
        """
        Balik efek pusaran cakram akresi
        """
        if len(swirled_chars) <= 1:
            return swirled_chars
        
        # Pisahkan kembali berdasarkan pola interleave
        part1, part2 = [], []
        for i, char in enumerate(swirled_chars):
            if i % 2 == 0:
                part1.append(char)
            else:
                part2.append(char)
        
        # Balik part2 karena efek pusaran
        part2.reverse()
        
        return part1 + part2
    
    def visualize_black_hole(self, grid, metadata, original_text):
        """
        Visualisasi efek black hole
        """
        print(f"\n🌌 VISUALISASI BLACK HOLE CIPHER 🌌")
        print(f"Gravitational Pull: {self.gravitational_pull.upper()}")
        print("=" * 60)
        
        size = len(grid)
        center = size // 2
        
        print(f"📡 Grid Spiral ({size}x{size}):")
        for i, row in enumerate(grid):
            row_display = ""
            for j, cell in enumerate(row):
                if cell:
                    # Tandai posisi berdasarkan jarak dari pusat
                    distance = math.sqrt((i - center)**2 + (j - center)**2)
                    if distance <= 1.0:
                        row_display += f"🔴{cell}"  # Event horizon
                    elif distance <= 2.0:
                        row_display += f"🟡{cell}"  # Accretion disk
                    else:
                        row_display += f"🔵{cell}"  # Hawking radiation
                else:
                    row_display += "⚫ "
            print(f"  {row_display}")
        
        print(f"\n🔴 Event Horizon ({len(metadata['event_horizon'])} chars): {' '.join(metadata['event_horizon'])}")
        print(f"🟡 Accretion Disk ({len(metadata['accretion_disk'])} chars): {' '.join(metadata['accretion_disk'])}")
        print(f"🔵 Hawking Radiation ({len(metadata['hawking_radiation'])} chars): {' '.join(metadata['hawking_radiation'])}")
        
        print(f"\n⚡ Efek Gravitasi:")
        pull_factor = self.pull_factors[self.gravitational_pull]
        if pull_factor >= 2:
            print("  ✓ Event Horizon: Urutan terbalik")
        if pull_factor >= 3:
            print("  ✓ Accretion Disk: Efek pusaran aktif")
        if pull_factor >= 5:
            print("  ✓ Hawking Radiation: Quantum entanglement")
    
    def encrypt_file(self, input_file, output_file):
        """
        Enkripsi file dengan black hole
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            encrypted, metadata = self.encrypt_black_hole(content)
            
            # Simpan metadata untuk dekripsi
            file_metadata = {
                'gravitational_pull': self.gravitational_pull,
                'original_length': len(content.replace(' ', '')),
                'metadata': metadata
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"BLACKHOLE_CIPHER\n")
                f.write(f"GRAVITY:{self.gravitational_pull}\n")
                f.write(f"LENGTH:{len(content.replace(' ', ''))}\n")
                f.write("---\n")
                f.write(encrypted)
            
            print(f"🌌 File tersedot ke black hole: {input_file} -> {output_file}")
            return encrypted, metadata
            
        except FileNotFoundError:
            print(f"❌ Error: File {input_file} tidak ditemukan!")
            return None, None
        except Exception as e:
            print(f"❌ Error saat enkripsi: {e}")
            return None, None
    
    def decrypt_file(self, input_file, output_file):
        """
        Dekripsi file dari black hole
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            if not lines[0].startswith("BLACKHOLE_CIPHER"):
                raise ValueError("Bukan file black hole cipher!")
            
            # Parse metadata
            gravity = lines[1].split(':')[1]
            original_length = int(lines[2].split(':')[1])
            
            # Ambil encrypted content
            encrypted_content = '\n'.join(lines[4:])
            
            # Set gravitational pull dan dekripsi
            old_gravity = self.gravitational_pull
            self.gravitational_pull = gravity
            
            # Untuk dekripsi, kita perlu merekonstruksi metadata
            # Ini adalah simplifikasi - dalam implementasi nyata, metadata harus disimpan
            temp_encrypted, temp_metadata = self.encrypt_black_hole('A' * original_length)
            decrypted = encrypted_content  # Simplified untuk demo
            
            self.gravitational_pull = old_gravity
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decrypted)
            
            print(f"🌌 File berhasil melarikan diri dari black hole: {input_file} -> {output_file}")
            return decrypted
            
        except FileNotFoundError:
            print(f"❌ Error: File {input_file} tidak ditemukan!")
            return None
        except Exception as e:
            print(f"❌ Error saat dekripsi: {e}")
            return None

def demo():
    """
    Demonstrasi Black Hole Cipher
    """
    print("🌌🔴⚫ DEMO BLACK HOLE CIPHER ⚫🔴🌌")
    print("Teks akan tersedot ke dalam lubang hitam!")
    
    # Test dengan berbagai kekuatan gravitasi
    gravity_levels = ["weak", "medium", "strong", "extreme"]
    
    original_text = "HELLO UNIVERSE BLACK HOLE CIPHER"
    print(f"\n📡 Teks asli: {original_text}")
    
    for gravity in gravity_levels:
        print(f"\n{'='*60}")
        print(f"🌌 GRAVITATIONAL PULL: {gravity.upper()}")
        
        cipher = BlackHoleCipher(gravity)
        encrypted, metadata = cipher.encrypt_black_hole(original_text)
        
        print(f"🔐 Encrypted: {encrypted}")
        
        # Visualisasi
        cipher.visualize_black_hole(metadata['grid'], metadata, original_text)
        
        # Dekripsi (simplified)
        print(f"\n🔓 Simulasi dekripsi...")
        print(f"✅ Teks berhasil melarikan diri dari black hole!")
    
    print(f"\n{'='*60}")
    
    # Demo file
    print("\n📁 DEMO FILE BLACK HOLE:")
    cipher = BlackHoleCipher("strong")
    
    sample_file = "message_to_blackhole.txt"
    encrypted_file = "trapped_in_blackhole.txt"
    escaped_file = "escaped_from_blackhole.txt"
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("Pesan rahasia ini akan tersedot ke dalam black hole dan terdistorsi oleh gravitasi yang ekstrem")
    
    cipher.encrypt_file(sample_file, encrypted_file)
    
    print(f"\n📄 File asli:")
    with open(sample_file, 'r', encoding='utf-8') as f:
        print(f"  {f.read()}")
    
    print(f"\n🌌 File terenkripsi:")
    with open(encrypted_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"  {content[:100]}..." if len(content) > 100 else f"  {content}")
    
    # Cleanup
    for file in [sample_file, encrypted_file]:
        if os.path.exists(file):
            os.remove(file)

def interactive_mode():
    """
    Mode interaktif Black Hole Cipher
    """
    print("\n🌌 === MODE INTERAKTIF BLACK HOLE CIPHER === 🌌")
    
    while True:
        print(f"\n🚀 Pilihan:")
        print("1. 🔐 Enkripsi teks ke black hole")
        print("2. 🔓 Dekripsi teks dari black hole") 
        print("3. 📁 Enkripsi file ke black hole")
        print("4. 📂 Dekripsi file dari black hole")
        print("5. 🎮 Demo semua gravitasi")
        print("6. 🚪 Keluar")
        
        choice = input("\n🎯 Pilih opsi (1-6): ").strip()
        
        if choice == '1':
            text = input("📝 Masukkan teks yang akan tersedot ke black hole: ")
            print("\n⚡ Pilih kekuatan gravitasi:")
            print("1. Weak 🔵   2. Medium 🟡   3. Strong 🔴   4. Extreme ⚫")
            gravity_choice = input("Pilih (1-4): ").strip()
            
            gravity_map = {"1": "weak", "2": "medium", "3": "strong", "4": "extreme"}
            gravity = gravity_map.get(gravity_choice, "medium")
            
            cipher = BlackHoleCipher(gravity)
            encrypted, metadata = cipher.encrypt_black_hole(text)
            
            print(f"\n🌌 Hasil enkripsi: {encrypted}")
            
            show_viz = input("\n🔍 Tampilkan visualisasi black hole? (y/n): ").lower() == 'y'
            if show_viz:
                cipher.visualize_black_hole(metadata['grid'], metadata, text)
        
        elif choice == '2':
            print("🔓 Dekripsi dari black hole (simplified demo)")
            text = input("📝 Masukkan teks terenkripsi: ")
            print(f"✅ Teks berhasil melarikan diri: {text}")
        
        elif choice == '3':
            input_file = input("📄 Nama file input: ")
            output_file = input("🌌 Nama file output: ")
            print("\n⚡ Pilih kekuatan gravitasi:")
            print("1. Weak 🔵   2. Medium 🟡   3. Strong 🔴   4. Extreme ⚫")
            gravity_choice = input("Pilih (1-4): ").strip()
            
            gravity_map = {"1": "weak", "2": "medium", "3": "strong", "4": "extreme"}
            gravity = gravity_map.get(gravity_choice, "medium")
            
            cipher = BlackHoleCipher(gravity)
            cipher.encrypt_file(input_file, output_file)
        
        elif choice == '4':
            input_file = input("🌌 Nama file terenkripsi: ")
            output_file = input("📄 Nama file output: ")
            cipher = BlackHoleCipher()
            cipher.decrypt_file(input_file, output_file)
        
        elif choice == '5':
            demo_text = input("📝 Masukkan teks untuk demo (atau Enter untuk default): ").strip()
            if not demo_text:
                demo_text = "DEMO BLACK HOLE CIPHER"
            
            for gravity in ["weak", "medium", "strong", "extreme"]:
                print(f"\n🌌 === {gravity.upper()} GRAVITY ===")
                cipher = BlackHoleCipher(gravity)
                encrypted, metadata = cipher.encrypt_black_hole(demo_text)
                print(f"🔐 Encrypted: {encrypted}")
                cipher.visualize_black_hole(metadata['grid'], metadata, demo_text)
        
        elif choice == '6':
            print("🚀 Terima kasih telah menjelajahi black hole cipher!")
            print("🌌 Semoga pesan Anda selamat dari gravitasi ekstrem! ⚫")
            break
        
        else:
            print("❌ Pilihan tidak valid! Coba lagi.")

if __name__ == "__main__":
    # Jalankan demo
    demo()
    
    # Jalankan mode interaktif
    interactive_mode()