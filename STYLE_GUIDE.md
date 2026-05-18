# Standar Komunikasi & Dokumentasi Backend

## Aturan Komentar (Code Comments)
*   **Tanpa Header File**: Dilarang meletakkan komentar atau docstring di baris paling atas file.
*   **Tanpa Karakter Dash**: Dilarang menggunakan tanda "-" (dash/hyphen), "–" (en-dash), atau "—" (em-dash) dalam komentar.
*   **Format**: Gunakan teks murni, tanda baca koma (,), atau titik dua (:) untuk pemisah.
*   **Gaya**: Singkat, padat, dan jelas.

## Aturan Pesan & Log (Messages & Logs)
*   **Bahasa**: Gunakan Bahasa Indonesia formal.
*   **Istilah Teknis**: Tetap gunakan istilah aslinya dalam Bahasa Inggris (contoh: *User*, *Database*, *Repository*, *Endpoint*, *Request*, *Payload*).
*   **Gaya**: Singkat dan langsung pada intinya.

### Contoh Transformasi:
*   *Lama*: `# --- Validasi User ---`
*   *Baru*: `# Validasi User:`
*   *Lama*: `return {"message": "User not found"}`
*   *Baru*: `return {"message": "User tidak ditemukan"}`
*   *Lama*: `logger.info("Successfully updated profile")`
*   *Baru*: `logger.info("Profil berhasil diperbarui")`
