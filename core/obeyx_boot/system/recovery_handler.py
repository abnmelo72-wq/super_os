# core/obeyx_boot/system/recovery_handler.py

import os
import shutil
import time
import hashlib
import zipfile
from ..utils.boot_logger import BootLogger

logger = BootLogger()

class RecoveryHandler:
    def __init__(self, backup_dir="/var/backups/super_os"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        logger.log("🔁 RecoveryHandler initialized with smart logic.")

    def _hash_folder(self, folder_path):
        """احسب هاش كامل للمجلد لتوثيق النسخة الاحتياطية"""
        sha = hashlib.sha256()
        for root, dirs, files in os.walk(folder_path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        while chunk := f.read(8192):
                            sha.update(chunk)
                except:
                    continue
        return sha.hexdigest()

    def _compress_backup(self, source_path, dest_zip):
        """ضغط النسخة الاحتياطية"""
        with zipfile.ZipFile(dest_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(source_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, start=source_path)
                    zf.write(full_path, arcname)

    def create_backup(self, path_to_backup, custom_name=None):
        """إنشاء نسخة احتياطية ذكية بضغط وتوثيق"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        name = custom_name or os.path.basename(path_to_backup)
        backup_name = f"{name}_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)

        try:
            shutil.copytree(path_to_backup, backup_path)
            hash_value = self._hash_folder(backup_path)

            zip_path = f"{backup_path}.zip"
            self._compress_backup(backup_path, zip_path)
            shutil.rmtree(backup_path)  # حذف الأصل بعد الضغط

            with open(f"{zip_path}.sha256", "w") as f:
                f.write(hash_value)

            logger.success(f"✅ Smart backup created: {zip_path}")
        except Exception as e:
            logger.error(f"❌ Smart backup failed: {e}")

    def restore_backup(self, backup_zip_name, target_path="/"):
        """استعادة النسخة الاحتياطية مع التحقق من صحتها"""
        zip_path = os.path.join(self.backup_dir, backup_zip_name)
        hash_path = zip_path + ".sha256"

        if not os.path.exists(zip_path):
            logger.error("❌ Backup zip not found.")
            return

        try:
            # فك الضغط مؤقتًا
            temp_dir = os.path.join(self.backup_dir, "temp_restore")
            os.makedirs(temp_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(temp_dir)

            # التحقق من الهاش
            actual_hash = self._hash_folder(temp_dir)
            with open(hash_path, "r") as f:
                expected_hash = f.read().strip()

            if actual_hash != expected_hash:
                logger.error("❌ Backup integrity check failed!")
                shutil.rmtree(temp_dir)
                return

            # نسخ للمسار الهدف
            for item in os.listdir(temp_dir):
                s = os.path.join(temp_dir, item)
                d = os.path.join(target_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            shutil.rmtree(temp_dir)
            logger.success(f"✅ Backup restored successfully from: {zip_path}")

        except Exception as e:
            logger.error(f"❌ Restore failed: {e}")
