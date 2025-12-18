#!/usr/bin/env python3
"""
Integrate parsed OCR logbook entries into website content.
Merges new entries with existing content.json while preserving structure.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

def load_json(filepath: Path) -> Any:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: Any, filepath: Path):
    """Save JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def integrate_logbook_entries(content: Dict, new_entries: List[Dict]) -> Dict:
    """Integrate new OCR entries into content.json."""
    
    print("="*70)
    print("INTEGRATING OCR ENTRIES INTO WEBSITE")
    print("="*70)
    
    # Get existing logbook entries
    existing_entries = content.get('logbook', [])
    print(f"Existing logbook entries: {len(existing_entries)}")
    print(f"New OCR entries to add: {len(new_entries)}")
    
    # Find the highest existing ID
    max_id = max([entry.get('id', 0) for entry in existing_entries], default=-1)
    
    # Renumber new entries starting from max_id + 1
    for idx, entry in enumerate(new_entries):
        entry['id'] = max_id + 1 + idx
    
    # Combine entries
    all_entries = existing_entries + new_entries
    
    # Sort by date (handle various date formats)
    def parse_date_for_sort(date_str):
        """Parse date string for sorting."""
        try:
            # Try ISO format first
            if '-' in date_str:
                parts = date_str.split('-')
                if len(parts) == 3:
                    year = int(parts[0]) if len(parts[0]) == 4 else int(parts[2])
                    month = int(parts[1])
                    day = int(parts[2]) if len(parts[0]) == 4 else int(parts[0])
                    return (year, month, day)
        except:
            pass
        # Default to end of list if date can't be parsed
        return (9999, 12, 31)
    
    all_entries.sort(key=lambda x: parse_date_for_sort(x.get('date', '9999-12-31')))
    
    # Update content
    content['logbook'] = all_entries
    
    print(f"Total logbook entries after integration: {len(all_entries)}")
    print("="*70)
    
    return content

def update_hero_section(content: Dict, statistics: Dict) -> Dict:
    """Update hero section with OCR statistics."""
    hero = content.get('hero', {})
    
    # Add OCR completion note
    ocr_note = (
        f"This website now includes {statistics.get('pages_with_content', 0)} "
        f"logbook entries extracted via OCR from the original {statistics.get('total_pages', 197)} "
        f"handwritten pages. Aircraft mentions: {statistics.get('aircraft_mentions', 0)}, "
        f"Squadron mentions: {statistics.get('squadron_mentions', 0)}."
    )
    
    hero['ocr_completion'] = ocr_note
    content['hero'] = hero
    
    return content

def generate_summary_report(original_content: Dict, updated_content: Dict, statistics: Dict):
    """Generate a summary report of the integration."""
    report = {
        'integration_timestamp': str(Path('data/content.json').stat().st_mtime),
        'original_entries': len(original_content.get('logbook', [])),
        'new_entries_added': len(updated_content.get('logbook', [])) - len(original_content.get('logbook', [])),
        'total_entries': len(updated_content.get('logbook', [])),
        'ocr_statistics': statistics,
    }
    
    return report

def main():
    """Main integration function."""
    print("\n" + "="*70)
    print("OCR CONTENT INTEGRATION")
    print("="*70 + "\n")
    
    # Check if parsed entries exist
    parsed_entries_file = Path("ocr_output/logbook_entries.json")
    if not parsed_entries_file.exists():
        print(f"ERROR: Parsed entries not found: {parsed_entries_file}")
        print("Please run parse_advanced.py first.")
        return
    
    statistics_file = Path("ocr_output/parsing_statistics.json")
    content_file = Path("data/content.json")
    
    # Load data
    print("Loading files...")
    new_entries = load_json(parsed_entries_file)
    statistics = load_json(statistics_file) if statistics_file.exists() else {}
    original_content = load_json(content_file)
    
    # Create backup
    backup_file = Path("data/content.json.backup")
    save_json(original_content, backup_file)
    print(f"✓ Backup created: {backup_file}")
    
    # Integrate
    updated_content = integrate_logbook_entries(original_content.copy(), new_entries)
    updated_content = update_hero_section(updated_content, statistics)
    
    # Save updated content
    save_json(updated_content, content_file)
    print(f"✓ Updated content saved: {content_file}")
    
    # Generate and save report
    report = generate_summary_report(original_content, updated_content, statistics)
    report_file = Path("ocr_output/integration_report.json")
    save_json(report, report_file)
    print(f"✓ Integration report saved: {report_file}")
    
    print("\n" + "="*70)
    print("INTEGRATION SUMMARY")
    print("="*70)
    print(f"Original entries: {report['original_entries']}")
    print(f"New entries added: {report['new_entries_added']}")
    print(f"Total entries: {report['total_entries']}")
    print(f"OCR pages processed: {statistics.get('total_pages', 0)}")
    print(f"Pages with content: {statistics.get('pages_with_content', 0)}")
    print("="*70)
    print("\n✓ Integration complete! Website content updated.")
    print(f"✓ Backup available at: {backup_file}")
    print("\nNext steps:")
    print("1. Review data/content.json")
    print("2. Test website locally: open index.html")
    print("3. Commit and push changes")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
