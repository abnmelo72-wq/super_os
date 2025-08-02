#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# obeyx_ai_core/smart_loader_pro.py
# نظام تحميل ذكي خارق - الإصدار الاحترافي

import os
import sys
import time
import threading
import importlib
import shutil
import psutil
import platform
import torch
import gc
import requests
import concurrent.futures
import json
import hashlib
import asyncio
import subprocess
import logging
import traceback
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Callable
from collections import OrderedDict, deque
from dataclasses import dataclass, field

# ===== إعدادات متقدمة =====
MAX_CONCURRENT_LOAD = 4  # أقصى عدد نماذج يتم تحميلها في نفس الوقت
MODEL_CACHE_SIZE = 5     # عدد النماذج التي تبقى في الذاكرة
LOW_POWER_THRESHOLD = 20 # نسبة البطارية المتبقية لتفعيل وضع التوفير
HIGH_TEMP_THRESHOLD = 75 # درجة الحرارة العظمى (مئوية) قبل تفعيل التبريد
PERFORMANCE_MODES = ['extreme', 'balanced', 'power_saver']
DEFAULT_PERFORMANCE_MODE = 'balanced'
MODEL_REPOSITORY = "https://models.obeyx.ai/v2/"

# ===== هياكل البيانات المتقدمة =====
@dataclass
class ModelMetadata:
    name: str
    version: str
    dependencies: List[str]
    memory_usage: float  # بالجيجابايت
    priority: int = 5    # 1-10 (10 = الأهم)
    last_used: float = 0
    load_count: int = 0

@dataclass
class SystemDiagnostics:
    cpu_usage: List[float] = field(default_factory=list)
    ram_usage: List[float] = field(default_factory=list)
    gpu_usage: List[float] = field(default_factory=list)
    network_usage: List[float] = field(default_factory=list)
    anomalies: List[Dict] = field(default_factory=list)

# ===== حالة النظام =====
loaded_models: Dict[str, Any] = OrderedDict()
model_metadata: Dict[str, ModelMetadata] = {}
system_report: Dict[str, Any] = {}
load_log: deque = deque(maxlen=1000)  # سجل دائري
error_log: deque = deque(maxlen=500)
optimization_flags: List[str] = []
model_response_times: Dict[str, float] = {}
live_status: Dict[str, Any] = {}
diagnostics_data = SystemDiagnostics()
performance_mode: str = DEFAULT_PERFORMANCE_MODE
model_cache = OrderedDict()  # LRU Cache للنماذج
adaptive_learning = {
    'model_usage_patterns': {},
    'system_behavior': {}
}

# ===== تسجيل متقدم =====
class SmartLogger:
    def __init__(self):
        self.logger = logging.getLogger('SmartLoaderPro')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', 
                                     datefmt='%Y-%m-%d %H:%M:%S')
        
        # تسجيل إلى ملف
        file_handler = logging.FileHandler('smart_loader.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # تسجيل إلى وحدة التحكم
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def log(self, msg: str, level: str = 'info'):
        stamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[SmartLoaderPro - {stamp}] {msg}"
        
        if level == 'info':
            self.logger.info(msg)
            load_log.append(entry)
        elif level == 'error':
            self.logger.error(msg)
            error_log.append(entry)
        elif level == 'warning':
            self.logger.warning(msg)
            load_log.append(f"[WARN] {entry}")
        elif level == 'debug':
            self.logger.debug(msg)
        
        # تحديث حالة النظام
        live_status['last_log'] = entry

logger = SmartLogger()

# ===== فحص بيئة النظام المتقدم =====
def scan_system() -> Dict[str, Any]:
    """فحص شامل للنظام مع جمع بيانات متقدمة"""
    try:
        # معلومات المعالج
        cpu_info = {
            'cores': psutil.cpu_count(logical=False),
            'logical_cores': psutil.cpu_count(logical=True),
            'usage': psutil.cpu_percent(interval=0.5),
            'freq': psutil.cpu_freq().current if hasattr(psutil, 'cpu_freq') else None
        }
        
        # معلومات الذاكرة
        mem = psutil.virtual_memory()
        ram_info = {
            'total': round(mem.total / (1024**3), 2),
            'available': round(mem.available / (1024**3), 2),
            'used': round(mem.used / (1024**3), 2),
            'percent': mem.percent
        }
        
        # معلومات GPU
        gpu_info = {}
        if torch.cuda.is_available():
            gpu_info = {
                'name': torch.cuda.get_device_name(0),
                'memory_total': round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2),
                'memory_allocated': round(torch.cuda.memory_allocated(0) / (1024**3), 2),
                'memory_cached': round(torch.cuda.memory_reserved(0) / (1024**3), 2)
            }
        
        # معلومات النظام
        os_info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine()
        }
        
        # معلومات الشبكة
        net_info = {
            'speed': get_network_speed(),
            'latency': get_network_latency()
        }
        
        # معلومات الطاقة
        power_info = get_power_status()
        
        # تحديث تقرير النظام
        system_report.update({
            'cpu': cpu_info,
            'ram': ram_info,
            'gpu': gpu_info,
            'os': os_info,
            'torch_version': torch.__version__,
            'python_version': platform.python_version(),
            'network': net_info,
            'power': power_info,
            'timestamp': time.time(),
            'performance_mode': performance_mode
        })
        
        logger.log(f"✅ System Scan: CPU={cpu_info['usage']}% | RAM={ram_info['used']}/{ram_info['total']}GB | GPU={gpu_info.get('name', 'None')}", 'info')
        return system_report
    except Exception as e:
        logger.log(f"System scan failed: {traceback.format_exc()}", 'error')
        return {}

def get_network_speed() -> float:
    """قياس سرعة الشبكة بدقة عالية"""
    try:
        test_file = "https://speedtest.obeyx.ai/100mb.test"
        start = time.perf_counter()
        with requests.get(test_file, stream=True, timeout=10) as r:
            r.raise_for_status()
            total_bytes = 0
            for chunk in r.iter_content(chunk_size=8192):
                total_bytes += len(chunk)
                if time.perf_counter() - start > 5:  # الحد الأقصى 5 ثوان
                    break
        elapsed = time.perf_counter() - start
        speed = (total_bytes / (1024**2)) / elapsed  # MB/s
        return round(speed, 2)
    except:
        return 0.0

def get_network_latency() -> float:
    """قياس زمن الوصول للشبكة"""
    try:
        target = "8.8.8.8"
        start = time.perf_counter()
        subprocess.run(["ping", "-c", "1", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        return round((time.perf_counter() - start) * 1000, 2)  # مللي ثانية
    except:
        return -1.0

def get_power_status() -> Dict[str, Any]:
    """الحصول على حالة الطاقة والنظام"""
    try:
        battery = psutil.sensors_battery() if hasattr(psutil, 'sensors_battery') else None
        return {
            'plugged': battery.power_plugged if battery else None,
            'percent': battery.percent if battery else None,
            'power_time': battery.secsleft if battery else None,
            'low_power': battery.percent < LOW_POWER_THRESHOLD if battery and battery.percent else False
        }
    except:
        return {}

# ===== نظام تحميل النماذج المتقدم =====
def load_model(name: str, priority: int = 5, preload_only: bool = False) -> Any:
    """تحميل النموذج مع إدارة ذكية للذاكرة"""
    start_time = time.perf_counter()
    
    # التحقق من وجود النموذج في ذاكرة التخزين المؤقت
    if name in model_cache:
        model = model_cache[name]
        model_metadata[name].last_used = time.time()
        model_metadata[name].load_count += 1
        logger.log(f"⚡️ Model '{name}' served from cache (Priority: {priority})", 'info')
        return model
    
    # التحقق من التبعيات
    if not check_dependencies(name):
        logger.log(f"❌ Model '{name}' dependencies not satisfied", 'error')
        return None
    
    # تحميل النموذج
    try:
        # تحميل ديناميكي للوحدة
        module_name = f"models.{name}_loader"
        model_module = importlib.import_module(module_name)
        
        # استدعاء دالة التحميل
        loader_func = getattr(model_module, f"load_{name}")
        
        # تحميل النموذج مع معلمات الأداء
        model = loader_func(performance_mode=performance_mode)
        
        # تسجيل النموذج
        loaded_models[name] = model
        model_cache[name] = model
        model_cache.move_to_end(name)  # تحديث الترتيب في ذاكرة التخزين المؤقت
        
        # تحديث البيانات الوصفية
        if name not in model_metadata:
            model_metadata[name] = ModelMetadata(
                name=name,
                version=get_model_version(name),
                dependencies=get_model_dependencies(name),
                memory_usage=estimate_model_memory(name, model),
                priority=priority
            )
        
        model_metadata[name].last_used = time.time()
        model_metadata[name].load_count += 1
        
        # تسجيل زمن التحميل
        elapsed = round(time.perf_counter() - start_time, 2)
        model_response_times[name] = elapsed
        logger.log(f"🔁 Model '{name}' loaded in {elapsed}s (Priority: {priority})", 'info')
        
        # التكيف مع نمط الاستخدام
        adaptive_learning['model_usage_patterns'][name] = adaptive_learning['model_usage_patterns'].get(name, 0) + 1
        
        return model if not preload_only else None
        
    except Exception as e:
        logger.log(f"Failed to load model '{name}': {traceback.format_exc()}", 'error')
        return None

def unload_model(name: str) -> bool:
    """تفريغ النموذج من الذاكرة"""
    try:
        if name in loaded_models:
            # تنظيف النموذج إذا كان يدعم ذلك
            if hasattr(loaded_models[name], 'cleanup'):
                loaded_models[name].cleanup()
            
            # حذف النموذج
            del loaded_models[name]
            
            # حذف من ذاكرة التخزين المؤقت
            if name in model_cache:
                del model_cache[name]
            
            logger.log(f"♻️ Unloaded model '{name}' to free memory", 'info')
            return True
        return False
    except Exception as e:
        logger.log(f"Failed to unload model '{name}': {e}", 'error')
        return False

def manage_model_cache() -> None:
    """إدارة ذاكرة التخزين المؤقت للنماذج بناءً على الاستخدام والذاكرة المتاحة"""
    # تفريغ النماذج الأقل استخدامًا عند الحاجة
    while len(model_cache) > MODEL_CACHE_SIZE:
        name, _ = model_cache.popitem(last=False)
        unload_model(name)
    
    # تفريغ إضافي عند انخفاض الذاكرة
    mem_available = system_report.get('ram', {}).get('available', 0)
    if mem_available < 1.0:  # أقل من 1GB متاحة
        logger.log("⚠️ Low memory detected - freeing model cache", 'warning')
        for name in list(model_cache.keys())[:-2]:  # الاحتفاظ بنموذجين فقط
            if name in model_cache:
                unload_model(name)

def check_dependencies(model_name: str) -> bool:
    """التحقق من تبعيات النموذج"""
    # محاكاة للتبعيات - في التنفيذ الحقيقي سيتم التحقق من التبعيات الفعلية
    required_deps = ['torch', 'transformers', 'numpy']
    for dep in required_deps:
        try:
            importlib.import_module(dep)
        except ImportError:
            logger.log(f"❌ Missing dependency '{dep}' for model '{model_name}'", 'error')
            return False
    return True

def get_model_version(model_name: str) -> str:
    """الحصول على إصدار النموذج (محاكاة)"""
    return "1.2.0"  # في التنفيذ الحقيقي سيتم قراءة من ملف تعريف

def get_model_dependencies(model_name: str) -> List[str]:
    """الحصول على تبعيات النموذج (محاكاة)"""
    return ['torch>=1.10', 'transformers>=4.18']  # في التنفيذ الحقيقي سيتم قراءة من ملف تعريف

def estimate_model_memory(model_name: str, model_obj: Any) -> float:
    """تقدير استخدام الذاكرة للنموذج"""
    # محاكاة - في التنفيذ الحقيقي سيتم قياس الذاكرة الفعلية
    if 'llm' in model_name:
        return 3.2
    elif 'vision' in model_name:
        return 1.8
    return 0.5

# ===== نظام التحميل المتوازي الذكي =====
def parallel_model_loader(model_list: List[Tuple[str, int]]) -> Dict[str, Any]:
    """تحميل متوازي للنماذج مع إدارة الأولويات"""
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_LOAD) as executor:
        # إنشاء مهام التحميل
        future_to_model = {
            executor.submit(load_model, name, priority): name 
            for name, priority in model_list
        }
        
        # معالجة النتائج عند اكتمالها
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                results[model_name] = future.result()
            except Exception as e:
                logger.log(f"Parallel load failed for {model_name}: {e}", 'error')
                results[model_name] = None
    
    # تقدير مستوى الذكاء
    estimate_intelligence_level()
    
    return results

# ===== التحسينات التلقائية المتقدمة =====
def auto_optimize_system() -> None:
    """التحسين التلقائي للنظام بناءً على الظروف الحالية"""
    try:
        # التحقق من درجة الحرارة
        if system_report.get('cpu', {}).get('temp', 0) > HIGH_TEMP_THRESHOLD:
            set_performance_mode('power_saver')
            logger.log("❄️ Enabled cooling mode due to high temperature", 'warning')
        
        # التحقق من حالة الطاقة
        power_status = system_report.get('power', {})
        if power_status.get('low_power', False):
            set_performance_mode('power_saver')
            logger.log("🔋 Enabled power saver mode", 'info')
        
        # التحقق من استخدام الذاكرة
        mem_usage = system_report.get('ram', {}).get('percent', 0)
        if mem_usage > 85:
            logger.log("⚠️ High memory usage - optimizing model cache", 'warning')
            manage_model_cache()
        
        # تحسين إعدادات Torch
        optimize_torch_settings()
        
        # تحميل نماذج متوقعة
        predict_and_preload_models()
        
    except Exception as e:
        logger.log(f"Auto-optimization failed: {e}", 'error')

def set_performance_mode(mode: str) -> None:
    """تغيير وضع الأداء للنظام"""
    global performance_mode
    if mode in PERFORMANCE_MODES:
        performance_mode = mode
        system_report['performance_mode'] = mode
        logger.log(f"⚙️ Performance mode changed to '{mode}'", 'info')
        
        # إعادة تحميل النماذج المتأثرة
        for model_name in list(model_cache.keys()):
            if model_metadata[model_name].priority >= 7:  # إعادة تحميل النماذج عالية الأولوية فقط
                unload_model(model_name)
                load_model(model_name, model_metadata[model_name].priority)
    else:
        logger.log(f"Invalid performance mode: {mode}", 'error')

def optimize_torch_settings() -> None:
    """تحسين إعدادات PyTorch للأداء الأمثل"""
    try:
        if torch.cuda.is_available():
            # التحسينات الخاصة بـ CUDA
            torch.backends.cudnn.benchmark = True
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # إدارة ذاكرة أفضل
            torch.cuda.empty_cache()
            
            logger.log("⚙️ Optimized CUDA settings for better performance", 'info')
        
        if torch.backends.mps.is_available():
            # التحسينات لأنظمة Apple Silicon
            torch.backends.mps.set_per_process_memory_fraction(0.75)
            logger.log("🍎 Optimized MPS settings for Apple Silicon", 'info')
    except Exception as e:
        logger.log(f"Torch optimization failed: {e}", 'error')

# ===== الذكاء الاصطناعي التكيفي =====
def predict_and_preload_models() -> None:
    """التنبؤ بالنماذج المطلوبة مسبقًا بناءً على أنماط الاستخدام"""
    try:
        # تحليل أنماط الاستخدام
        usage_patterns = adaptive_learning.get('model_usage_patterns', {})
        if not usage_patterns:
            return
        
        # العثور على النماذج الأكثر استخدامًا
        sorted_models = sorted(usage_patterns.items(), key=lambda x: x[1], reverse=True)
        
        # تحميل مسبق للنماذج المتوقعة
        for model_name, count in sorted_models[:2]:  # تحميل مسبق لنموذجين
            if model_name not in model_cache:
                logger.log(f"🔮 Pre-loading predicted model: {model_name}", 'info')
                load_model(model_name, priority=6, preload_only=True)
    except Exception as e:
        logger.log(f"Predictive pre-load failed: {e}", 'error')

def estimate_intelligence_level() -> None:
    """تقدير مستوى ذكاء النظام بناءً على قدراته"""
    try:
        # حساب زمن التحميل الإجمالي
        total_load_time = sum(model_response_times.values())
        
        # تحليل قدرات النظام
        capabilities = []
        if torch.cuda.is_available():
            capabilities.append('gpu_acceleration')
        if len(loaded_models) > 3:
            capabilities.append('multi_model')
        if adaptive_learning.get('model_usage_patterns'):
            capabilities.append('predictive_loading')
        
        # تحديد مستوى الذكاء
        if 'gpu_acceleration' in capabilities and total_load_time < 5:
            level = "⚡ فائق الذكاء"
            score = 95
        elif len(capabilities) > 2 and total_load_time < 8:
            level = "🧠 ذكي جداً"
            score = 85
        elif len(capabilities) > 1:
            level = "🧠 ذكي"
            score = 75
        else:
            level = "🌀 عادي"
            score = 60
        
        # تحديث تقرير النظام
        system_report['intelligence_level'] = level
        system_report['intelligence_score'] = score
        system_report['capabilities'] = capabilities
        
        logger.log(f"🧠 Estimated AI Level: {level} (Score: {score})", 'info')
    except Exception as e:
        logger.log(f"Intelligence estimation failed: {e}", 'error')

# ===== المراقبة والتحليل المتقدم =====
async def realtime_monitor() -> None:
    """مراقبة النظام في الوقت الحقيقي"""
    while True:
        try:
            # تحديث حالة النظام
            scan_system()
            
            # جمع بيانات التشخيص
            diagnostics_data.cpu_usage.append(psutil.cpu_percent())
            diagnostics_data.ram_usage.append(psutil.virtual_memory().percent)
            
            if torch.cuda.is_available():
                diagnostics_data.gpu_usage.append(torch.cuda.utilization())
            
            # الكشف عن الشذوذ
            detect_anomalies()
            
            # تحديث حالة النظام الحي
            update_live_status()
            
            # الانتظار للدورة التالية
            await asyncio.sleep(2.5)
            
        except Exception as e:
            logger.log(f"Realtime monitor error: {e}", 'error')
            await asyncio.sleep(5)

def detect_anomalies() -> None:
    """الكشف عن السلوك غير الطبيعي في النظام"""
    try:
        # الكشف عن ارتفاع غير طبيعي في استخدام وحدة المعالجة المركزية
        if len(diagnostics_data.cpu_usage) > 10:
            last_10 = diagnostics_data.cpu_usage[-10:]
            avg = sum(last_10) / len(last_10)
            if diagnostics_data.cpu_usage[-1] > avg * 1.5:
                anomaly = {
                    'type': 'high_cpu',
                    'value': diagnostics_data.cpu_usage[-1],
                    'timestamp': time.time()
                }
                diagnostics_data.anomalies.append(anomaly)
                logger.log(f"⚠️ CPU spike detected: {diagnostics_data.cpu_usage[-1]}%", 'warning')
        
        # الكشف عن ارتفاع غير طبيعي في درجة الحرارة
        if system_report.get('cpu', {}).get('temp', 0) > HIGH_TEMP_THRESHOLD:
            anomaly = {
                'type': 'high_temp',
                'value': system_report['cpu']['temp'],
                'timestamp': time.time()
            }
            diagnostics_data.anomalies.append(anomaly)
            logger.log(f"🌡️ High temperature detected: {system_report['cpu']['temp']}°C", 'warning')
    except Exception as e:
        logger.log(f"Anomaly detection failed: {e}", 'error')

def update_live_status() -> None:
    """تحديث حالة النظام الحي"""
    live_status.update({
        'timestamp': time.time(),
        'models_loaded': list(model_cache.keys()),
        'model_count': len(model_cache),
        'memory_usage': psutil.virtual_memory().percent,
        'cpu_usage': psutil.cpu_percent(),
        'performance_mode': performance_mode,
        'last_anomaly': diagnostics_data.anomalies[-1] if diagnostics_data.anomalies else None
    })

# ===== واجهات النظام المتقدمة =====
def export_diagnostics(filename: str = "system_diagnostics.json") -> bool:
    """تصدير بيانات التشخيص إلى ملف"""
    try:
        data = {
            'system_report': system_report,
            'loaded_models': list(model_cache.keys()),
            'model_metadata': {name: vars(md) for name, md in model_metadata.items()},
            'performance_mode': performance_mode,
            'intelligence_level': system_report.get('intelligence_level', 'N/A'),
            'diagnostics': {
                'cpu_usage': diagnostics_data.cpu_usage,
                'ram_usage': diagnostics_data.ram_usage,
                'anomalies': diagnostics_data.anomalies
            },
            'logs': list(load_log),
            'errors': list(error_log),
            'export_time': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.log(f"📊 Exported diagnostics to {filename}", 'info')
        return True
    except Exception as e:
        logger.log(f"Diagnostics export failed: {e}", 'error')
        return False

def generate_health_report() -> Dict[str, Any]:
    """إنشاء تقرير صحة النظام"""
    health_score = 100
    
    # خصم على أساس الأخطاء
    error_count = len(error_log)
    if error_count > 10:
        health_score -= 15
    elif error_count > 5:
        health_score -= 10
    elif error_count > 0:
        health_score -= 5
    
    # خصم على أساس الشذوذ
    anomaly_count = len(diagnostics_data.anomalies)
    if anomaly_count > 5:
        health_score -= 20
    elif anomaly_count > 2:
        health_score -= 10
    elif anomaly_count > 0:
        health_score -= 5
    
    # خصم على أساس الذاكرة
    if system_report.get('ram', {}).get('percent', 0) > 90:
        health_score -= 15
    
    # التأكد من أن النتيجة ضمن الحدود
    health_score = max(0, min(100, health_score))
    
    return {
        'health_score': health_score,
        'status': 'excellent' if health_score >= 90 else 
                 'good' if health_score >= 75 else 
                 'fair' if health_score >= 60 else 
                 'poor',
        'issue_count': error_count + anomaly_count,
        'last_scan': system_report.get('timestamp', 0),
        'recommendations': generate_recommendations(health_score)
    }

def generate_recommendations(health_score: int) -> List[str]:
    """توليد توصيات بناءً على صحة النظام"""
    recommendations = []
    
    if health_score < 90:
        recommendations.append("Consider upgrading hardware for better performance")
    
    if system_report.get('ram', {}).get('percent', 0) > 85:
        recommendations.append("Increase system RAM or optimize model memory usage")
    
    if len(error_log) > 5:
        recommendations.append("Review error logs and address recurring issues")
    
    if not recommendations:
        recommendations.append("System is well optimized. No critical recommendations")
    
    return recommendations

# ===== التهيئة والتشغيل =====
def initialize_system() -> None:
    """تهيئة النظام الذكي"""
    try:
        logger.log("🚀 Starting SmartLoader Pro - Advanced AI Loading System", 'info')
        
        # الفحص الأولي للنظام
        scan_system()
        
        # التحسين التلقائي الأولي
        auto_optimize_system()
        
        # تحميل النماذج الأساسية
        essential_models = [
            ('whisper', 9),
            ('llm_core', 10),
            ('vision_base', 8),
            ('audio_processor', 7)
        ]
        parallel_model_loader(essential_models)
        
        # بدء المراقبة في الوقت الحقيقي
        asyncio.create_task(realtime_monitor())
        
        # تنظيف الذاكرة الأولي
        smart_cleanup()
        
        logger.log("✅ SmartLoader Pro initialized successfully. System is operational 🔥", 'info')
        
        # إنشاء تقرير الصحة
        health = generate_health_report()
        logger.log(f"📈 System Health: {health['health_score']}/100 ({health['status']})", 'info')
        
    except Exception as e:
        logger.log(f"System initialization failed: {traceback.format_exc()}", 'error')
        sys.exit(1)

def smart_cleanup(full: bool = False) -> None:
    """تنظيف ذكي للذاكرة"""
    try:
        # تنظيف ذاكرة Python
        gc.collect()
        
        # تنظيف ذاكرة GPU إن وجدت
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        
        # تنظيف شامل إذا طُلب
        if full:
            for name in list(model_cache.keys()):
                if model_metadata[name].priority < 8:  # الاحتفاظ بالنماذج عالية الأولوية
                    unload_model(name)
        
        logger.log("🧹 Performed advanced memory cleanup", 'info')
    except Exception as e:
        logger.log(f"Memory cleanup failed: {e}", 'error')

# ===== الواجهة الرئيسية =====
if __name__ == "__main__":
    # تهيئة النظام
    initialize_system()
    
    # استمرار التشغيل للحفاظ على المهام الخلفية
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logger.log("🛑 SmartLoader Pro stopped by user", 'info')
        export_diagnostics()
        sys.exit(0)
