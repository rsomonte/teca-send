import os
import subprocess
import logging
from pathlib import Path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

logger = logging.getLogger(__name__)

class FileConverter:
    """Handle ebook file conversion using Calibre's ebook-convert"""
    
    SUPPORTED_FORMATS = config.SUPPORTED_FORMATS
    OUTPUT_FORMAT = config.OUTPUT_FORMAT
    
    @staticmethod
    def is_supported(file_path: str) -> bool:
        """Check if file format is supported"""
        ext = Path(file_path).suffix.lower().lstrip('.')
        return ext in FileConverter.SUPPORTED_FORMATS
    
    @staticmethod
    def convert(input_file: str, output_file: str) -> bool:
        """
        Convert ebook file to Kindle format using ebook-convert
        
        Args:
            input_file: Path to input ebook file
            output_file: Path to output ebook file
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            if not os.path.exists(input_file):
                logger.error(f"Input file not found: {input_file}")
                return False
            
            logger.info(f"Starting conversion: {input_file} -> {output_file}")
            
            # Use Calibre's ebook-convert command
            cmd = [
                'ebook-convert',
                input_file,
                output_file,
                '--margin-left=0',
                '--margin-right=0',
                '--margin-top=0',
                '--margin-bottom=0',
                '--no-colors',
                '--paper-size=a6',
                '--disable-markup-chapter-headings',
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.error(f"Conversion failed: {result.stderr}")
                return False
            
            logger.info(f"Conversion completed successfully: {output_file}")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("Conversion timed out after 300 seconds")
            return False
        except Exception as e:
            logger.error(f"Conversion error: {str(e)}")
            return False
    
    @staticmethod
    def get_output_filename(input_filename: str) -> str:
        """Get output filename with new extension"""
        base_name = Path(input_filename).stem
        return f"{base_name}.{FileConverter.OUTPUT_FORMAT}"
