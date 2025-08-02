#!/bin/bash

echo "🔄 جاري تنظيم مشروع super_os ..."

# إنشاء المجلدات المنظمة
mkdir -p obeyx_ai_core/brain
mkdir -p obeyx_ai_core/commands
mkdir -p obeyx_ai_core/perception
mkdir -p system_core/kernel
mkdir -p system_core/drivers
mkdir -p system_core/user_interface

# نقل ملفات معروفة إلى أماكنها الجديدة (عدّل حسب الملفات الموجودة فعليًا عندك)
mv boot_sequence.py obeyx_ai_core/ 2>/dev/null
mv smart_loader.py obeyx_ai_core/ 2>/dev/null
mv brain.py obeyx_ai_core/brain/ 2>/dev/null
mv commands.py obeyx_ai_core/commands/ 2>/dev/null
mv voice_module.py obeyx_ai_core/perception/ 2>/dev/null
mv audio_listener.py obeyx_ai_core/perception/ 2>/dev/null
mv image_vision.py obeyx_ai_core/perception/ 2>/dev/null
mv kernel.c system_core/kernel/ 2>/dev/null
mv tty.c system_core/kernel/ 2>/dev/null
mv drivers/* system_core/drivers/ 2>/dev/null
mv ui_main.py system_core/user_interface/ 2>/dev/null

# إنشاء ملف .gitignore لتجاهل ملفات غير ضرورية
cat <<EOF > .gitignore
venv-super/
__pycache__/
*.pyc
*.log
*.swp
EOF

# تحديث git
git add .
git commit -m "📁 إعادة تنظيم مشروع super_os: فصل ObeyX عن النظام"
git push

echo "✅ تمت إعادة التنظيم بنجاح!"
