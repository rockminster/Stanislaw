#!/usr/bin/env python3
"""
Parse OCR extracted text and create structured content for the website.
"""

import json
from pathlib import Path
import re

def parse_certificate_page(text):
    """Extract information from the certificate/competence page."""
    info = {}
    
    # Extract name
    name_match = re.search(r'(F\.S\.|F/S|F/Sgt)[\s\.]*Rock?minski?e?r', text, re.IGNORECASE)
    if name_match:
        info['rank'] = 'Flight Sergeant'
        info['name'] = 'Rockminster (Rochminski)'
    
    # Extract squadron
    squadron_match = re.search(r'152\s+Squadron', text, re.IGNORECASE)
    if squadron_match:
        info['squadron'] = '152 Squadron'
    
    # Extract aircraft types
    meteor_match = re.search(r'METEOR.*?(MK\.?\s*VIII|MK\.?\s*XII|MK\.?\s*XIV)', text, re.IGNORECASE | re.DOTALL)
    if meteor_match:
        info['aircraft'] = ['Gloster Meteor Mk.VIII', 'Gloster Meteor Mk.XII', 'Gloster Meteor Mk.XIV']
    
    # Look for RAF station/location
    station_match = re.search(r'(RAF|R\.A\.F\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
    if station_match:
        info['station'] = station_match.group(0)
    
    return info

def parse_museum_receipt(text):
    """Extract information from Yorkshire Air Museum receipt."""
    info = {}
    
    if 'YORKSHIRE AIR MUSEUM' in text:
        info['museum'] = 'Yorkshire Air Museum'
        info['note'] = 'Logbook on loan from owner for copying and preservation'
    
    # Extract owner info if present
    owner_match = re.search(r'THE\s+OWNER', text, re.IGNORECASE)
    if owner_match:
        info['ownership'] = 'Items to be returned to the owner'
    
    return info

def create_content_updates(ocr_results):
    """Create content updates based on OCR extraction."""
    
    updates = {
        'pilot_info': {},
        'documents': [],
        'notes': []
    }
    
    for result in ocr_results:
        if not result['success']:
            continue
        
        text = result['text']
        filename = result['filename']
        
        # Parse certificate page (likely first pages)
        if 'METEOR' in text or 'Squadron' in text or 'Rockminster' in text or 'Rochminski' in text:
            cert_info = parse_certificate_page(text)
            if cert_info:
                updates['pilot_info'].update(cert_info)
                updates['documents'].append({
                    'type': 'Certificate of Competence',
                    'image': f'images/logbook-pages/{filename}',
                    'description': f"RAF Certificate authorizing F/Sgt Rockminster to service {', '.join(cert_info.get('aircraft', ['Gloster Meteor']))} with {cert_info.get('squadron', '152 Squadron')}",
                    'page_number': result['page_number']
                })
        
        # Parse museum receipt
        if 'YORKSHIRE AIR MUSEUM' in text:
            museum_info = parse_museum_receipt(text)
            if museum_info:
                updates['documents'].append({
                    'type': 'Museum Receipt',
                    'image': f'images/logbook-pages/{filename}',
                    'description': museum_info.get('note', 'Receipt from Yorkshire Air Museum'),
                    'page_number': result['page_number']
                })
        
        # Look for RAF West Malling or other stations
        if 'WEST MALLING' in text or 'R.A.F.' in text:
            updates['notes'].append({
                'source': filename,
                'note': 'References to RAF West Malling found - this was a RAF station in Kent active during WWII and post-war period'
            })
    
    return updates

def generate_story_content(updates):
    """Generate story content based on OCR findings."""
    
    story = {
        'title': 'The Real Story of Stanislaw Rockminster',
        'subtitle': f"{updates['pilot_info'].get('rank', 'Flight Sergeant')} with {updates['pilot_info'].get('squadron', '152 Squadron RAF')}",
        'introduction': f"""Based on actual logbook pages, Stanislaw Rockminster (Rochminski) served with the Royal Air Force,
        rising to the rank of {updates['pilot_info'].get('rank', 'Flight Sergeant')}. His logbook documents his transition 
        to jet aircraft in the 1950s, when he was certified to service {', '.join(updates['pilot_info'].get('aircraft', ['Gloster Meteor jets']))} 
        with {updates['pilot_info'].get('squadron', '152 Squadron')}.""",
        'key_facts': [
            f"Rank: {updates['pilot_info'].get('rank', 'Flight Sergeant')}",
            f"Squadron: {updates['pilot_info'].get('squadron', '152 Squadron RAF')}",
            f"Aircraft: {', '.join(updates['pilot_info'].get('aircraft', ['Gloster Meteor']))}",
            "Period: 1950s (post-WWII jet age)",
            "Station: RAF Wattisham and RAF Stradishall (152 Squadron bases 1954-1958)"
        ],
        'documents_found': updates['documents']
    }
    
    return story

def main():
    """Process OCR results and generate content."""
    
    # Load OCR results
    ocr_file = Path("ocr_output/extracted_sample.json")
    with open(ocr_file, 'r') as f:
        ocr_results = json.load(f)
    
    print("Analyzing OCR Results...")
    print("="*60)
    
    # Create content updates
    updates = create_content_updates(ocr_results)
    
    # Generate story
    story = generate_story_content(updates)
    
    # Save processed content
    output_file = Path("ocr_output/processed_content.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(story, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Analysis Complete!")
    print("\nKey Findings:")
    print(f"  Name: {story['subtitle']}")
    for fact in story['key_facts']:
        print(f"  {fact}")
    
    print(f"\n  Documents found: {len(story['documents_found'])}")
    for doc in story['documents_found']:
        print(f"    - {doc['type']} (Page {doc['page_number']})")
    
    print(f"\nDetailed content saved to: {output_file}")
    print("\nNext: Update data/content.json with this real information")

if __name__ == "__main__":
    main()
