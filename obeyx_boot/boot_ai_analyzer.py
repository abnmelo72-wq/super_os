# super_os/obeyx_boot/boot_ai_analyzer.py

import time
import traceback
from obeyx_boot.core.modules.memory import short_term_memory, knowledge_graph, knowledge_accumulator
from obeyx_boot.core.modules.logic import LogicalReasoner, CausalInferencer
from obeyx_boot.core.modules.language import advanced_nlp
from obeyx_boot.core.modules.tools import tool_registry, AutoCodeFixer
from obeyx_boot.core.modules.context import SystemContext
from obeyx_boot.core.modules.future_interface import AIProgrammingToolset
from obeyx_boot.core.modules.user_insight import EmotionDetector, BehaviorPredictor

class ObeyXBootAIAnalyzer:
    def __init__(self):
        self.memory = short_term_memory
        self.knowledge_graph = knowledge_graph
        self.accumulator = knowledge_accumulator
        self.reasoner = LogicalReasoner()
        self.causal_inferencer = CausalInferencer()
        self.context = SystemContext()
        self.toolset = AIProgrammingToolset()
        self.code_fixer = AutoCodeFixer()
        self.emotion_analyzer = EmotionDetector()
        self.behavior_predictor = BehaviorPredictor()
        self.debug_mode = True

    def log(self, message):
        if self.debug_mode:
            print(f"[BOOT_ANALYZER_LOG] {message}")

    def analyze_boot(self, input_data, user_voice_sample=None):
        try:
            self.log("🚀 بدء تحليل ذكي متعدد الطبقات...")

            # التفكير المنطقي
            logic_result = self.reasoner.evaluate(input_data)
            self.log(f"🧠 نتيجة التفكير المنطقي: {logic_result}")

            # التفكير السببي
            causal_factors = self.causal_inferencer.infer(input_data)
            self.log(f"🔗 استنتاج الأسباب المحتملة: {causal_factors}")

            # تحديث الذاكرة و قاعدة المعرفة
            self.memory.store("boot_input", input_data)
            self.knowledge_graph.update_node("boot_sequence", input_data)
            self.accumulator.add_entry("boot_session", {
                "input": input_data,
                "logic": logic_result,
                "causal": causal_factors
            })

            # تحليل مشاعر المستخدم (اختياري: إذا وُجد صوت)
            emotion = None
            if user_voice_sample:
                emotion = self.emotion_analyzer.analyze(user_voice_sample)
                self.log(f"❤️ المشاعر المكتشفة: {emotion}")

            # تحليل السلوك وتوقع النية
            behavior_intent = self.behavior_predictor.predict(self.context, input_data)
            self.log(f"🤖 نية المستخدم المتوقعة: {behavior_intent}")

            # التحقق من مشاكل أو أخطاء
            if "خطأ" in input_data or "مشكلة" in input_data:
                fix = self.reasoner.suggest_solution(input_data)
                code_fix = self.code_fixer.attempt_fix(input_data)
                self.log(f"🛠️ حلول مقترحة: {fix}, تصحيح برمجي: {code_fix}")
                return {
                    "status": "issue_detected",
                    "analysis": logic_result,
                    "causal": causal_factors,
                    "suggested_fix": fix,
                    "auto_code_fix": code_fix,
                    "emotion": emotion,
                    "predicted_behavior": behavior_intent
                }

            # تهيئة أدوات الذكاء البرمجي
            tools_ready = self.toolset.initialize_tools()
            self.log(f"🧰 أدوات البرمجة الذكية جاهزة: {tools_ready}")

            return {
                "status": "success",
                "analysis": logic_result,
                "causal": causal_factors,
                "tools": tools_ready,
                "emotion": emotion,
                "predicted_behavior": behavior_intent
            }

        except Exception as e:
            self.log("🚨 حدث استثناء أثناء التحليل:")
            self.log(traceback.format_exc())
            return {
                "status": "error",
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
