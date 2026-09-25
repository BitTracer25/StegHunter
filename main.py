import sys
import os
from stego.engine import StegHunter

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_image>")
        sys.exit(1)

    target_image = sys.argv[1]
    hunter = StegHunter(target_image)
    
    print(f"\n--- Analyzing: {os.path.basename(target_image)} ---")
    results = hunter.run_full_analysis()
    
    if results:
        # 1. Probability
        print(f"[*] Combined model score (mean): {results['combined_score']*100:.2f}%")
        for model_name, score in results.get("model_scores", {}).items():
            print(f"[*] {model_name.replace('_', ' ').title()} score: {score*100:.2f}%")
        if results.get("model_errors"):
            print(f"[!] Model loading/inference issues: {results['model_errors']}")
        
        # 2. LSB Results
        if results['lsb_data']:
            preview = results['lsb_data'][:100].replace('\n', ' ')
            print(f"[*] LSB Extraction Preview: {preview}...")
        
        # 3. Metadata Results
        print("\n[*] Scanning Metadata...")
        if results['metadata']:
            for item in results['metadata']:
                print(f"    - {item}")
        else:
            print("    - No metadata found.")

        # 4. EOF Results
        print("\n[*] Scanning End-of-File (EOF)...")
        if results['eof_data']:
            # Try to decode EOF data as text
            try:
                decoded_eof = results['eof_data'].decode('utf-8', errors='ignore')
                print(f"    - Found trailing data: {decoded_eof[:100]}...")
            except:
                print(f"    - Found binary trailing data ({len(results['eof_data'])} bytes)")
        else:
            print("    - No trailing data found.")
            
    else:
        print("[!] Analysis failed.")

if __name__ == "__main__":
    main()
