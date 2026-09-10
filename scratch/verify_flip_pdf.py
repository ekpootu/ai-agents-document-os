import pypdf

pdf_path = 'no-commit/Book_Flip_Through_Video_Creator_Guide.pdf'
reader = pypdf.PdfReader(pdf_path)
num_pages = len(reader.pages)
print(f"Total Pages: {num_pages}")

p1 = reader.pages[0]
w = float(p1.mediabox.width)
h = float(p1.mediabox.height)
ratio = h / w
print(f"Dimensions: {w:.2f} pt x {h:.2f} pt ({w/72:.2f}\" x {h/72:.2f}\")")
print(f"Aspect Ratio: {ratio:.4f} (Target 1.6000)")

# Check TOC links on page 2
p2 = reader.pages[1]
annots = p2.get('/Annots', [])
print(f"Page 2 (TOC) link annotations count: {len(annots)}")

# Check target resolution
dest_dict = reader.named_destinations
print(f"Named destinations found: {len(dest_dict)}")
for name, dest in dest_dict.items():
    # dest can be an explicit destination
    try:
        page_num = reader.get_destination_page_number(dest)
        print(f"  Destination '{name}' -> Page {page_num + 1}")
    except Exception as e:
        print(f"  Destination '{name}' -> Error: {e}")
