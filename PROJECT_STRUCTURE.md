# 🧠 Super OS - Project Structure Map

---

## 🌐 super_os (Root System)

📁 super_os/
│
├── 📁 core/                  ← ملفات نظام التشغيل الأساسية (kernel-like)
│   ├── boot.c
│   ├── system.c
│
├── 📁 drivers/               ← تعريفات الصوت، الكاميرا، الشبكة...
│   ├── audio_driver.py
│   ├── gpu_driver.py
│
├── 📁 gui/                   ← واجهة المستخدم الرسومية
│   ├── window_manager.py
│   ├── terminal_ui.py
│
├── 📁 ai_core/               ← المحرك الذكائي العام
│   ├── 📁 commands/          ← تحليل الأوامر (صوتية، كتابية)
│   ├── 📁 models/            ← Whisper, Vosk, GPT interfaces
│   ├── 📁 language/          ← تحليل اللغة، ترجمة
│   ├── tools.py             ← أدوات مساعدة
│
├── 📁 obeyx_core/            ← قلب ObeyX الذكي
│   ├── brain.py             ← اتخاذ قرارات
│   ├── dispatcher.py        ← توزيع المهام
│   ├── personality.py       ← شخصية ObeyX (أنثى/ذكر/سلوك)
│   ├── vision.py            ← (لاحقًا) رؤية آلية
│
├── 📁 utils/                 ← أدوات مساعدة لكل النظام
│   ├── logger.py
│   ├── error_handler.py
│
├── 📁 config/                ← إعدادات النظام والمساعد
│   ├── system_config.json
│   ├── obeyx_config.json
│
├── main.py                  ← نقطة التشغيل الأساسية للنظام
├── start.sh                 ← سكربت تشغيل النظام الذكي
├── requirements.txt         ← المكتبات المطلوبة
├── README.md
├── PROJECT_STRUCTURE.md     ← هذا الملف


---

