#!/usr/bin/env python3
"""
verify_round_with_your_seeds.py

Educational verifier for a provably-fair dice-style roll.
You provided:
  - client_seed = "pxfv6pdY0X"
  - published_commitment = "6691b3a8b89b96292a9f930343af4690dd4892db29d5af87ac6f6f4bce346fcf"

Usage:
  - To run the demo fallback (no server seed provided):
      python verify_round_with_your_seeds.py
    This will show the published commitment and instruct you.

  - To verify a revealed server seed:
      python verify_round_with_your_seeds.py --server "REVEALED_SERVER_SEED"
    Or provide nonce:
      python verify_round_with_your_seeds.py --server "REVEALED_SERVER_SEED" --nonce 5

Ethical note: Use this only to VERIFY rounds after the server seed has been REVEALED.
"""

import hashlib
import hmac
import binascii
import argparse
import sys

# --- Pasteed values from user ---
CLIENT_SEED = "pxfv6pdY0X"
PUBLISHED_COMMITMENT = "6691b3a8b89b96292a9f930343af4690dd4892db29d5af87ac6f6f4bce346fcf"
# ----------------------------------

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def hmac_sha256_hex(key: str, message: str) -> str:
    h = hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    return h.hexdigest()

def roll_from_seeds(server_seed: str, client_seed: str, nonce: int) -> float:
    """
    Deterministic roll algorithm (educational):
      - HMAC-SHA256 with key = server_seed, message = client_seed + ":" + str(nonce)
      - Use first 8 bytes of HMAC output -> 64-bit integer
      - Map to 0..9999 then divide by 100 to get 0.00 - 99.99
    """
    message = f"{client_seed}:{nonce}"
    hmac_hex = hmac_sha256_hex(server_seed, message)
    hmac_bytes = binascii.unhexlify(hmac_hex)
    part = hmac_bytes[:8]
    value = int.from_bytes(part, byteorder='big')
    roll100 = value % 10000
    roll = roll100 / 100.0
    return roll

def compute_commitment(server_seed: str) -> str:
    return sha256_hex(server_seed)

def verify_round(published_commitment: str, server_seed: str, client_seed: str, nonce: int) -> bool:
    computed_commit = compute_commitment(server_seed)
    print(f"Published commitment: {published_commitment}")
    print(f"Computed commitment:  {computed_commit}")
    if computed_commit != published_commitment:
        print("\n>>> VERIFICATION FAILED: The provided server_seed does NOT match the published commitment.")
        return False
    else:
        print("\nCommitment verified: server_seed matches the published commitment.")
        roll = roll_from_seeds(server_seed, client_seed, nonce)
        print(f"Deterministic roll for client_seed='{client_seed}', nonce={nonce} -> {roll:.2f}")
        return True

def main():
    parser = argparse.ArgumentParser(description="Verify a provably-fair round using your client seed and a revealed server seed.")
    parser.add_argument("--server", "-s", help="Revealed server seed (string). If omitted, the script will only display your pasted values.")
    parser.add_argument("--nonce", "-n", type=int, default=1, help="Nonce / round number (default: 1).")
    parser.add_argument("--client", "-c", default=CLIENT_SEED, help=f"Client seed (default uses the pasted client seed: {CLIENT_SEED})")
    parser.add_argument("--published", "-p", default=PUBLISHED_COMMITMENT, help="Published commitment (hex SHA256 of server seed).")
    args = parser.parse_args()

    print("=== Provably-Fair Verifier ===")
    print(f"Using client seed: {args.client}")
    print(f"Using published commitment: {args.published}")
    print()

    if not args.server:
        print("No server seed provided. To verify a round, run with --server \"REVEALED_SERVER_SEED\"")
        print("Example:")
        print("  python verify_round_with_your_seeds.py --server \"your-server-seed-here\" --nonce 1")
        sys.exit(0)

    # Verify
    ok = verify_round(args.published, args.server, args.client, args.nonce)
    if ok:
        print("\nVerification completed successfully.")
    else:
        print("\nVerification FAILED. Do not trust the result if server seed and published commitment mismatch.")

if __name__ == "__main__":
    main()
from fpdf import FPDF

# Custom PDF class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Comprehensive Report on Tulsi (Holy Basil)", ln=True, align="C")
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_fill_color(255, 255, 153)  # light yellow background
pdf.rect(0, 0, 210, 297, 'F')

# --- Title Page ---
pdf.set_font("Arial", "B", 24)
pdf.cell(0, 80, "TULSI (HOLY BASIL) REPORT", ln=True, align="C")
pdf.set_font("Arial", "", 14)
pdf.cell(0, 10, "Prepared by: Student Name", ln=True, align="C")
pdf.cell(0, 10, "Submitted to: ____________", ln=True, align="C")
pdf.cell(0, 10, "Date: October 2025", ln=True, align="C")
pdf.ln(40)

# --- Certificate ---
pdf.set_font("Arial", "B", 20)
pdf.cell(0, 10, "Certificate", ln=True, align="C")
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
This is to certify that the report titled 'Tulsi (Holy Basil)' has been completed
and submitted by the student as part of their academic work. The report includes
complete information about the Tulsi plant, its medicinal properties, and its
historical and spiritual importance in Hinduism.
""")
pdf.ln(10)

# --- Acknowledgement ---
pdf.set_font("Arial", "B", 20)
pdf.cell(0, 10, "Acknowledgement", ln=True, align="C")
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
I would like to express my sincere gratitude to my teachers, family members,
and friends who supported and encouraged me during the preparation of this
report on the Tulsi plant. I also thank all the sources of information that helped
me understand the cultural and medicinal aspects of Tulsi in detail.
""")
pdf.ln(10)

# --- Report Body ---
pdf.add_page()
pdf.rect(0, 0, 210, 297, 'F')

# Helper to add headings
def add_heading(title):
    pdf.set_font("Arial", "BU", 30)
    pdf.cell(0, 20, title, ln=True)
    pdf.ln(5)

pdf.set_font("Arial", "", 12)

sections = {
    "Introduction": """The Tulsi plant, scientifically known as Ocimum tenuiflorum or Ocimum sanctum, is a sacred herb revered in Hinduism and valued in Ayurveda for its healing and spiritual benefits.""",
    "Botanical Description": """Tulsi is a small aromatic shrub from the mint family (Lamiaceae). It has green or purple leaves, fragrant flowers, and thrives in warm climates.""",
    "Historical & Mythological Context": """In Hindu mythology, Tulsi is worshipped as Goddess Vrinda, a devoted consort of Lord Vishnu. Tulsi Vivah, the ceremonial marriage to Vishnu, marks the start of the wedding season.""",
    "Medicinal Properties": """Tulsi contains essential oils and antioxidants such as eugenol and ursolic acid. It helps treat colds, fevers, respiratory disorders, stress, and infections.""",
    "Modern Applications": """Today, Tulsi is used in teas, herbal medicines, skincare, and aromatherapy. It is also being studied for its anti-diabetic, anti-cancer, and immune-boosting potential.""",
    "Conclusion": """Tulsi represents the union of spirituality and science—honoured as a goddess in Hindu homes and valued as a potent adaptogen in modern medicine."""
}

for title, content in sections.items():
    add_heading(title)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)
    pdf.ln(10)

pdf.output("Tulsi_Report.pdf")
print("✅ Tulsi_Report.pdf created successfully!")

from fpdf import FPDF

# Custom PDF class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Comprehensive Report on Tulsi (Holy Basil)", ln=True, align="C")
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_fill_color(255, 255, 153)  # yellow background
pdf.rect(0, 0, 210, 297, 'F')

# Title Page
pdf.set_font("Arial", "B", 24)
pdf.cell(0, 80, "TULSI (HOLY BASIL) REPORT", ln=True, align="C")
pdf.set_font("Arial", "", 14)
pdf.cell(0, 10, "Prepared by: Anushka", ln=True, align="C")
pdf.cell(0, 10, "Submitted to: Anu", ln=True, align="C")
pdf.cell(0, 10, "Date: October 2025", ln=True, align="C")
pdf.ln(40)

# Certificate
pdf.set_font("Arial", "B", 20)
pdf.cell(0, 10, "Certificate", ln=True, align="C")
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
This is to certify that the report titled 'Tulsi (Holy Basil)' has been completed
and submitted by Anushka as part of her academic work. The report includes
complete information about the Tulsi plant, its medicinal properties, and its
historical and spiritual importance in Hinduism.
""")
pdf.ln(10)

# Acknowledgement
pdf.set_font("Arial", "B", 20)
pdf.cell(0, 10, "Acknowledgement", ln=True, align="C")
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 10, """
I would like to express my sincere gratitude to my teacher Anu for her constant
guidance and encouragement during the preparation of this report. I also thank
my family members and friends for their support. This report is dedicated to
all who respect and value the sacred Tulsi plant.
""")
pdf.ln(10)

# Add new page for content
pdf.add_page()
pdf.rect(0, 0, 210, 297, 'F')

# Helper function to add headings
def add_heading(title):
    pdf.set_font("Arial", "BU", 30)
    pdf.cell(0, 20, title, ln=True)
    pdf.ln(5)

pdf.set_font("Arial", "", 12)

# Content sections
sections = {
    "Introduction": """The Tulsi plant, scientifically known as Ocimum tenuiflorum or Ocimum sanctum, is one of the most sacred plants in India. It holds immense cultural, spiritual, and medicinal value. It is revered not just as a plant but as a goddess — the manifestation of Goddess Vrinda. Tulsi plays a central role in Ayurvedic medicine and Hindu rituals.""",
    "Botanical Description": """Tulsi belongs to the Lamiaceae family and is a small aromatic shrub with green or purple leaves. It grows in tropical and subtropical regions and thrives in sunlight with moderate watering. The plant emits a strong, soothing fragrance due to its essential oils.""",
    "Historical & Mythological Context": """According to Hindu scriptures like the Padma Purana and the Skanda Purana, Tulsi is believed to be the earthly form of the goddess Vrinda, who was devoted to Lord Vishnu. The festival of Tulsi Vivah celebrates the symbolic marriage of Tulsi to Lord Vishnu, marking the beginning of the Hindu wedding season.""",
    "Medicinal Properties": """Tulsi is known for its remarkable healing properties. It acts as an adaptogen, helping the body manage stress. Its anti-inflammatory, antimicrobial, and antioxidant properties make it beneficial in treating colds, fevers, respiratory problems, and digestive disorders. Tulsi tea is commonly consumed for immunity and wellness.""",
    "Modern Applications": """Modern research has validated many traditional uses of Tulsi. It is used in herbal teas, supplements, essential oils, and skincare products. Scientific studies have shown that compounds like eugenol and ursolic acid in Tulsi can help reduce inflammation, control blood sugar, and enhance immunity.""",
    "Conclusion": """Tulsi represents the union of science and spirituality. Worshipped as a goddess and used as a powerful herbal remedy, Tulsi continues to hold a unique place in Indian culture and modern wellness practices. Caring for a Tulsi plant is both an act of devotion and a step toward natural healing and environmental harmony."""
}

for title, content in sections.items():
    add_heading(title)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)
    pdf.ln(10)

pdf.output("Tulsi_Report_Anushka.pdf")
print("✅ Tulsi_Report_Anushka.pdf created successfully!")
