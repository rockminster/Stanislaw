#!/usr/bin/env python3
"""
Advanced OCR content parser for RAF logbook entries.
Extracts structured data from OCR text and integrates into website content.
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class LogbookParser:
    """Parse OCR-extracted logbook text into structured entries."""
    
    # Common RAF terms and patterns
    AIRCRAFT_PATTERNS = [
        r'Meteor\s*(?:Mk\.?\s*)?([IVXLCDM]+)',
        r'Hurricane\s*(?:Mk\.?\s*)?([IVXLCDM]+)?',
        r'Spitfire\s*(?:Mk\.?\s*)?([IVXLCDM]+)?',
        r'Lancaster',
        r'Wellington',
        r'Mosquito',
        r'Typhoon',
        r'Tempest',
    ]
    
    RANK_PATTERNS = [
        r'F/?Sgt',
        r'Flight\s+Sergeant',
        r'Sgt',
        r'Sergeant',
        r'P/?O',
        r'Pilot\s+Officer',
        r'F/?Lt',
        r'Flight\s+Lieutenant',
        r'F/?O',
        r'Flying\s+Officer',
        r'W/?O',
        r'Warrant\s+Officer',
    ]
    
    SQUADRON_PATTERNS = [
        r'(\d{1,3})\s*Squadron',
        r'No\.?\s*(\d{1,3})\s*Sq',
        r'Squadron\s*(\d{1,3})',
    ]
    
    DATE_PATTERNS = [
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',  # DD/MM/YYYY or DD-MM-YY
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',    # YYYY/MM/DD
        r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{2,4})',
    ]
    
    def __init__(self, ocr_results_path: str):
        """Initialize parser with OCR results."""
        with open(ocr_results_path, 'r', encoding='utf-8') as f:
            self.ocr_data = json.load(f)
        
        self.parsed_entries = []
        self.statistics = {
            'total_pages': len(self.ocr_data),
            'pages_with_content': 0,
            'aircraft_mentions': 0,
            'squadron_mentions': 0,
            'dates_found': 0,
        }
    
    def extract_aircraft(self, text: str) -> List[str]:
        """Extract aircraft mentions from text."""
        aircraft = []
        for pattern in self.AIRCRAFT_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                aircraft_name = match.group(0)
                if aircraft_name not in aircraft:
                    aircraft.append(aircraft_name)
        return aircraft
    
    def extract_squadron(self, text: str) -> Optional[str]:
        """Extract squadron number from text."""
        for pattern in self.SQUADRON_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)} Squadron"
        return None
    
    def extract_rank(self, text: str) -> Optional[str]:
        """Extract rank from text."""
        for pattern in self.RANK_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def extract_dates(self, text: str) -> List[str]:
        """Extract dates from text."""
        dates = []
        for pattern in self.DATE_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                dates.append(match.group(0))
        return dates
    
    def extract_flight_duration(self, text: str) -> Optional[str]:
        """Extract flight duration (hours:minutes)."""
        # Look for time patterns like 1:30, 2.5, etc.
        patterns = [
            r'(\d+):(\d+)',  # 1:30
            r'(\d+)\.(\d+)\s*hrs?',  # 1.5 hrs
            r'(\d+)\s+hrs?\s+(\d+)\s+mins?',  # 1 hr 30 min
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def extract_base_location(self, text: str) -> Optional[str]:
        """Extract RAF base or location mentions."""
        # Common RAF base patterns
        base_patterns = [
            r'RAF\s+([A-Z][a-zA-Z]+)',
            r'Station\s+([A-Z][a-zA-Z]+)',
        ]
        for pattern in base_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
    
    def classify_entry_type(self, text: str) -> str:
        """Classify the type of logbook entry."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['certificate', 'certification', 'qualified', 'authorization']):
            return 'certification'
        elif any(word in text_lower for word in ['training', 'practice', 'exercise']):
            return 'training'
        elif any(word in text_lower for word in ['operation', 'mission', 'sortie', 'patrol']):
            return 'operational'
        elif any(word in text_lower for word in ['test', 'check', 'inspection']):
            return 'test_flight'
        elif any(word in text_lower for word in ['ferry', 'delivery', 'transport']):
            return 'ferry'
        else:
            return 'general'
    
    def parse_page(self, page_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse a single OCR page into structured entry."""
        if not page_data.get('success') or not page_data.get('text'):
            return None
        
        text = page_data['text']
        
        # Extract all relevant information
        aircraft = self.extract_aircraft(text)
        squadron = self.extract_squadron(text)
        rank = self.extract_rank(text)
        dates = self.extract_dates(text)
        duration = self.extract_flight_duration(text)
        base = self.extract_base_location(text)
        entry_type = self.classify_entry_type(text)
        
        # Update statistics
        if aircraft:
            self.statistics['aircraft_mentions'] += len(aircraft)
        if squadron:
            self.statistics['squadron_mentions'] += 1
        if dates:
            self.statistics['dates_found'] += len(dates)
        
        # Create structured entry
        entry = {
            'page_number': page_data['page_number'],
            'filename': page_data['filename'],
            'raw_text': text,
            'char_count': page_data.get('char_count', 0),
            'aircraft': aircraft,
            'squadron': squadron,
            'rank': rank,
            'dates': dates,
            'duration': duration,
            'base': base,
            'entry_type': entry_type,
            'ocr_extracted': True,
            'processing_time': page_data.get('processing_time', 0),
        }
        
        return entry
    
    def parse_all(self) -> List[Dict[str, Any]]:
        """Parse all OCR pages."""
        print("="*70)
        print("PARSING OCR RESULTS")
        print("="*70)
        print(f"Total pages to parse: {len(self.ocr_data)}")
        print()
        
        for page_data in self.ocr_data:
            entry = self.parse_page(page_data)
            if entry:
                self.parsed_entries.append(entry)
                self.statistics['pages_with_content'] += 1
                
                # Show progress every 20 pages
                if len(self.parsed_entries) % 20 == 0:
                    print(f"Parsed {len(self.parsed_entries)} pages...")
        
        print()
        print("="*70)
        print("PARSING COMPLETE")
        print("="*70)
        print(f"Pages with content: {self.statistics['pages_with_content']}/{self.statistics['total_pages']}")
        print(f"Aircraft mentions: {self.statistics['aircraft_mentions']}")
        print(f"Squadron mentions: {self.statistics['squadron_mentions']}")
        print(f"Dates found: {self.statistics['dates_found']}")
        print("="*70)
        
        return self.parsed_entries
    
    def generate_logbook_entries(self) -> List[Dict[str, Any]]:
        """Generate formatted logbook entries for website."""
        entries = []
        
        for idx, parsed in enumerate(self.parsed_entries):
            # Skip pages with very little content (likely blank or covers)
            if parsed['char_count'] < 100:
                continue
            
            # Create a readable title
            title_parts = []
            if parsed['aircraft']:
                title_parts.append(f"{', '.join(parsed['aircraft'][:2])}")
            if parsed['entry_type'] != 'general':
                title_parts.append(parsed['entry_type'].replace('_', ' ').title())
            
            title = ' - '.join(title_parts) if title_parts else f"Logbook Entry #{parsed['page_number']}"
            
            # Create description from first few lines
            lines = parsed['raw_text'].split('\n')
            description_lines = [line.strip() for line in lines if line.strip()][:3]
            description = ' '.join(description_lines[:2])
            if len(description) > 200:
                description = description[:200] + '...'
            
            # Determine date (use first date found or use a placeholder)
            date = parsed['dates'][0] if parsed['dates'] else f"1956-01-{parsed['page_number']:02d}"
            
            entry = {
                'id': len(entries),
                'date': date,
                'title': title,
                'description': description,
                'aircraft': ', '.join(parsed['aircraft']) if parsed['aircraft'] else 'Various',
                'duration': parsed['duration'] or 'N/A',
                'pilot': parsed['rank'] or 'F/Sgt Rockminster',
                'type': parsed['entry_type'],
                'image': f"images/logbook-pages/{parsed['filename']}",
                'ocr_extracted': True,
                'squadron': parsed['squadron'],
                'base': parsed['base'],
                'note': f"Extracted from logbook page {parsed['page_number']} via OCR. {parsed['char_count']} characters extracted.",
            }
            
            entries.append(entry)
        
        return entries
    
    def save_results(self, output_dir: Path):
        """Save parsed results."""
        output_dir.mkdir(exist_ok=True)
        
        # Save parsed entries
        parsed_file = output_dir / "parsed_entries.json"
        with open(parsed_file, 'w', encoding='utf-8') as f:
            json.dump(self.parsed_entries, f, indent=2, ensure_ascii=False)
        print(f"Saved parsed entries to: {parsed_file}")
        
        # Generate and save logbook entries for website
        logbook_entries = self.generate_logbook_entries()
        logbook_file = output_dir / "logbook_entries.json"
        with open(logbook_file, 'w', encoding='utf-8') as f:
            json.dump(logbook_entries, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(logbook_entries)} logbook entries to: {logbook_file}")
        
        # Save statistics
        stats_file = output_dir / "parsing_statistics.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.statistics, f, indent=2)
        print(f"Saved statistics to: {stats_file}")
        
        return logbook_entries

def main():
    """Main parsing function."""
    ocr_results_file = Path("ocr_output/extracted_all_pages.json")
    
    if not ocr_results_file.exists():
        print(f"ERROR: OCR results file not found: {ocr_results_file}")
        print("Please run extract_all_pages.py first.")
        return
    
    parser = LogbookParser(str(ocr_results_file))
    parser.parse_all()
    
    output_dir = Path("ocr_output")
    logbook_entries = parser.save_results(output_dir)
    
    print()
    print("="*70)
    print("NEXT STEPS")
    print("="*70)
    print("1. Review parsed entries in: ocr_output/parsed_entries.json")
    print("2. Logbook entries ready for website: ocr_output/logbook_entries.json")
    print("3. Update data/content.json with new entries")
    print("="*70)

if __name__ == "__main__":
    main()
