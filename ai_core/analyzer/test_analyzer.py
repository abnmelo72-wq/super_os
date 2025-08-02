from analyzer_main import analyze_command

while True:
    user_input = input("🧠 أدخل أمرًا ليتم تحليله: ")
    result = analyze_command(user_input)
    print("📊 تحليل الأمر:", result)
