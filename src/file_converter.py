import os
import subprocess
import logging
from pathlib import Path
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

logger = logging.getLogger(__name__)

class FileConverter:
    """Handle ebook file conversion using Calibre's ebook-convert"""
    
    SUPPORTED_FORMATS = os.getenv('SUPPORTED_FORMATS', 'epub,mobi,azw3').split(',')
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'mobi')
    
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

            input_size = os.path.getsize(input_file)
            if input_size == 0:
                logger.error(f"Input file is empty: {input_file}")
                return False
            
            logger.info(f"Starting conversion: {input_file} -> {output_file}")
            
            # Use Calibre's ebook-convert command with optional formatting flags.
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

            # Some Calibre builds do not support every optional flag.
            if result.returncode != 0 and 'no such option' in (result.stderr or '').lower():
                logger.warning(
                    "Calibre rejected one or more optional flags; retrying with a minimal command"
                )
                cmd = ['ebook-convert', input_file, output_file]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                logger.error(f"Conversion failed: {result.stderr}")
                return False

            if not FileConverter._is_valid_output_file(output_file):
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

    @staticmethod
    def _is_valid_output_file(output_file: str) -> bool:
        """Validate that conversion output exists and is readable by Calibre tools."""
        if not os.path.exists(output_file):
            logger.error(f"Conversion output file not found: {output_file}")
            return False

        output_size = os.path.getsize(output_file)
        if output_size == 0:
            logger.error(f"Conversion output file is empty: {output_file}")
            return False

        # Corrupted outputs are often tiny and unreadable by Kindle/Calibre.
        if output_size < 1024:
            logger.error(
                f"Conversion output is suspiciously small ({output_size} bytes): {output_file}"
            )
            return False

        ext = Path(output_file).suffix.lower()
        if ext == '.mobi':
            try:
                with open(output_file, 'rb') as f:
                    header = f.read(78)
                if len(header) < 78:
                    logger.error(f"MOBI output header too short: {output_file}")
                    return False
                # MOBI files should include the BOOKMOBI signature around offset 60.
                if header[60:68] != b'BOOKMOBI':
                    logger.error(
                        f"MOBI signature missing from converted output: {output_file}"
                    )
                    return False
            except Exception as e:
                logger.error(f"Failed to inspect MOBI header: {str(e)}")
                return False

        try:
            meta_result = subprocess.run(
                ['ebook-meta', output_file],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if meta_result.returncode != 0:
                logger.error(
                    "Converted output failed ebook-meta validation: "
                    f"{meta_result.stderr or meta_result.stdout}"
                )
                return False
        except FileNotFoundError:
            logger.warning("ebook-meta not found; skipping metadata validation")
        except subprocess.TimeoutExpired:
            logger.error("ebook-meta timed out while validating converted output")
            return False
        except Exception as e:
            logger.error(f"Unexpected output validation error: {str(e)}")
            return False

        return True
