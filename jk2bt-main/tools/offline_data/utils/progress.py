"""
进度显示工具
"""
import sys
from datetime import datetime


class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self, total: int, desc: str = "Processing"):
        self.total = total
        self.desc = desc
        self.current = 0
        self.success = 0
        self.failed = 0
        self.skipped = 0
        self.start_time = None
        
    def start(self):
        """开始跟踪"""
        self.start_time = datetime.now()
        self._print_progress()
    
    def update(self, success: bool = True, skipped: bool = False):
        """更新进度"""
        self.current += 1
        if skipped:
            self.skipped += 1
        elif success:
            self.success += 1
        else:
            self.failed += 1
        self._print_progress()
    
    def _print_progress(self):
        """打印进度"""
        if self.total == 0:
            return
        
        percent = self.current / self.total * 100
        bar_len = 30
        filled = int(bar_len * self.current / self.total)
        bar = "=" * filled + "-" * (bar_len - filled)
        
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        eta = elapsed / self.current * (self.total - self.current) if self.current > 0 else 0
        
        status = f"S:{self.success} F:{self.failed} K:{self.skipped}"
        
        sys.stdout.write(f"\r{self.desc}: [{bar}] {self.current}/{self.total} ({percent:.1f}%) {status} ETA:{eta:.0f}s")
        sys.stdout.flush()
        
        if self.current >= self.total:
            print()
    
    def finish(self):
        """完成"""
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        print(f"\n完成: {self.success} 成功, {self.failed} 失败, {self.skipped} 跳过, 耗时 {elapsed:.1f}s")
        
    def get_summary(self) -> dict:
        """获取摘要"""
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        return {
            "total": self.total,
            "success": self.success,
            "failed": self.failed,
            "skipped": self.skipped,
            "elapsed_seconds": elapsed,
        }
