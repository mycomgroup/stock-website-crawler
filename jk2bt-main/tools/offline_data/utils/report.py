"""
预热报告生成工具
"""
import os
import json
from datetime import datetime
from typing import Dict, List


class PrewarmReport:
    """预热报告生成器"""
    
    def __init__(self, report_dir: str = "reports/prewarm"):
        self.report_dir = report_dir
        self.results = {}
        self.start_time = datetime.now()
        
    def add_result(self, category: str, result: dict):
        """添加结果"""
        if category not in self.results:
            self.results[category] = []
        self.results[category].append(result)
    
    def set_summary(self, category: str, summary: dict):
        """设置摘要"""
        if category not in self.results:
            self.results[category] = {}
        self.results[category]["summary"] = summary
    
    def generate(self) -> str:
        """生成报告"""
        os.makedirs(self.report_dir, exist_ok=True)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "results": self.results,
        }
        
        # 保存 JSON 报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = os.path.join(self.report_dir, f"prewarm_report_{timestamp}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成文本报告
        txt_file = os.path.join(self.report_dir, f"prewarm_report_{timestamp}.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("离线数据预热报告\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"生成时间: {report['generated_at']}\n")
            f.write(f"总耗时: {report['duration_seconds']:.1f}秒\n\n")
            
            for category, data in self.results.items():
                f.write(f"\n{category}:\n")
                if "summary" in data:
                    s = data["summary"]
                    f.write(f"  成功: {s.get('success', 0)}\n")
                    f.write(f"  失败: {s.get('failed', 0)}\n")
                    f.write(f"  跳过: {s.get('skipped', 0)}\n")
            
            f.write("\n" + "=" * 60 + "\n")
        
        return json_file
