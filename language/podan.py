import polib
from deep_translator import GoogleTranslator
import argparse
from tqdm import tqdm
import time

def translate_po_file(input_file, output_file):
    """
    Translate a PO/POT file to Danish using Google Translate.
    
    Args:
        input_file (str): Path to input PO/POT file
        output_file (str): Path to output PO file
    """
    # Load the PO file
    po = polib.pofile(input_file)
    translator = GoogleTranslator(source='en', target='da')
    
    print(f"Found {len(po)} strings to translate")
    
    # Translate each untranslated entry
    for entry in tqdm(po):
        if not entry.msgstr:  # Only translate if no translation exists
            try:
                # Handle plural forms
                if entry.msgid_plural:
                    # Translate singular form
                    entry.msgstr_plural[0] = translator.translate(entry.msgid)
                    # Translate plural form
                    entry.msgstr_plural[1] = translator.translate(entry.msgid_plural)
                else:
                    # Translate regular string
                    entry.msgstr = translator.translate(entry.msgid)
                
                # Add a small delay to avoid rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error translating '{entry.msgid}': {str(e)}")
                continue
    
    # Save the translated file
    print(f"\nAbout to save file as: {output_file}")
    po.save(output_file)
    print(f"\nTranslation completed. Output saved to: {output_file}")

def main() -> Literal[1] | Literal[0]:
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Translate WordPress PO/POT files to Danish')
    parser.add_argument('input_file', help='Input PO/POT file path')
    parser.add_argument('--output', '-o', help='Output file path (default: input_file_da.po)',
                      default=None)
    
    args = parser.parse_args()
    
    # Generate output filename if not specified
    if not args.output:
        output_file = args.input_file.rsplit('.', 1)[0] + '_da.po'
    else:
        output_file = args.output
    
    print(f"\nWill save the file as {output_file}")

    try:
        translate_po_file(args.input_file, output_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

# %%
if __name__ == "__main__":
    main()