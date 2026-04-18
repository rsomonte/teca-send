import os
import shutil
import logging
from pathlib import Path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

logger = logging.getLogger(__name__)

class KindleTransfer:
    """Handle file transfer to connected Kindle device"""
    
    MOUNT_POINT = config.KINDLE_MOUNT_POINT
    DOCUMENTS_FOLDER = config.KINDLE_DOCUMENTS_FOLDER
    
    @staticmethod
    def is_kindle_connected() -> bool:
        """Check if Kindle device is connected and mounted"""
        try:
            mount_point = Path(KindleTransfer.MOUNT_POINT)
            if not mount_point.exists():
                logger.info(f"Kindle mount point does not exist: {KindleTransfer.MOUNT_POINT}")
                return False
            
            # Check if it's a mounted filesystem
            if not os.path.ismount(KindleTransfer.MOUNT_POINT):
                logger.info(f"Kindle mount point is not mounted: {KindleTransfer.MOUNT_POINT}")
                return False
            
            logger.info("Kindle device is connected")
            return True
        except Exception as e:
            logger.error(f"Error checking Kindle connection: {str(e)}")
            return False
    
    @staticmethod
    def get_kindle_documents_path() -> str:
        """Get path to Kindle documents folder"""
        doc_path = os.path.join(
            KindleTransfer.MOUNT_POINT,
            KindleTransfer.DOCUMENTS_FOLDER
        )
        return doc_path
    
    @staticmethod
    def transfer_file(file_path: str) -> bool:
        """
        Transfer converted file to Kindle device
        
        Args:
            file_path: Path to file to transfer
            
        Returns:
            True if transfer successful, False otherwise
        """
        try:
            if not KindleTransfer.is_kindle_connected():
                logger.warning("Kindle device is not connected")
                return False
            
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False
            
            kindle_docs = KindleTransfer.get_kindle_documents_path()
            os.makedirs(kindle_docs, exist_ok=True)
            
            file_name = os.path.basename(file_path)
            destination = os.path.join(kindle_docs, file_name)
            
            logger.info(f"Transferring file to Kindle: {file_name}")
            shutil.copy2(file_path, destination)
            
            logger.info(f"File successfully transferred to Kindle: {destination}")
            return True
            
        except PermissionError:
            logger.error("Permission denied when accessing Kindle device")
            return False
        except Exception as e:
            logger.error(f"Error transferring file to Kindle: {str(e)}")
            return False
