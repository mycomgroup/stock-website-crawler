#!/usr/bin/env python3
"""完整测试 setup.py 的工作流程"""

import sys
import os
import shutil
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_setup_workflow():
    """测试完整的 setup.py 工作流程"""
    print("=" * 60)
    print("测试 setup.py 完整工作流程")
    print("=" * 60)
    
    # 创建测试目录
    test_dir = Path("test_experiment_20260416")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    # 模拟命令行参数
    sys.argv = [
        "setup.py",
        "--name", "test_prescreen",
        "--start-date", "2018-01-01",
        "--end-date", "2023-12-31",
        "--pool", "HS300",
        "--prescreen",
        "--target-factors", "120",
        "--top-k", "5"
    ]
    
    try:
        # 导入并运行 setup.py
        import setup
        
        # 保存原始的 main 函数
        original_main = setup.main
        
        # 创建测试用的 main 函数
        def test_main():
            try:
                original_main()
                return True
            except Exception as e:
                print(f"运行 setup.py 时出错: {e}")
                return False
        
        # 替换 main 函数
        setup.main = test_main
        
        # 运行 setup.py
        print("\n运行 setup.py...")
        success = setup.main()
        
        if success and test_dir.exists():
            print(f"\n✓ 实验目录创建成功: {test_dir}")
            
            # 检查生成的文件
            expected_files = [
                "strategy.py",
                "seed_config.json",
                "strategy_pool.json",
                "search_notes.md",
                "prescreen_report.json"
            ]
            
            for file in expected_files:
                file_path = test_dir / file
                if file_path.exists():
                    print(f"✓ 文件已生成: {file}")
                    
                    # 检查 strategy.py 中的因子数量
                    if file == "strategy.py":
                        content = file_path.read_text(encoding="utf-8")
                        # 查找 FACTOR_COMBO
                        import re
                        match = re.search(r"FACTOR_COMBO\s*=\s*(\[.*?\])", content, re.DOTALL)
                        if match:
                            import ast
                            try:
                                factor_list = ast.literal_eval(match.group(1))
                                print(f"  strategy.py 中包含 {len(factor_list)} 个因子")
                                if len(factor_list) == 120:
                                    print("  ✓ 因子数量正确 (120个)")
                                else:
                                    print(f"  ✗ 因子数量不正确: 期望120, 实际{len(factor_list)}")
                            except:
                                print("  ✗ 无法解析因子列表")
                else:
                    print(f"✗ 文件缺失: {file}")
            
            # 检查 seed_config.json
            config_file = test_dir / "seed_config.json"
            if config_file.exists():
                import json
                config = json.loads(config_file.read_text(encoding="utf-8"))
                print(f"\n种子配置信息:")
                print(f"  预筛选启用: {config.get('prescreen_enabled', False)}")
                print(f"  目标因子数: {config.get('target_factors', 0)}")
                print(f"  总因子数: {config.get('all_factors_count', 0)}")
                print(f"  筛选后因子数: {config.get('screened_factors_count', 0)}")
            
            # 检查 prescreen_report.json
            report_file = test_dir / "prescreen_report.json"
            if report_file.exists():
                import json
                report = json.loads(report_file.read_text(encoding="utf-8"))
                print(f"\n预筛选报告:")
                print(f"  总因子数: {report.get('total_factors', 0)}")
                print(f"  筛选后因子数: {report.get('screened_factors', 0)}")
                print(f"  筛选方法: {report.get('screening_method', 'N/A')}")
                
                # 验证因子列表
                screened_list = report.get('screened_factor_list', [])
                if len(screened_list) == 120:
                    print(f"  ✓ 筛选报告中的因子数量正确 (120个)")
                else:
                    print(f"  ✗ 筛选报告中的因子数量不正确: 期望120, 实际{len(screened_list)}")
            
            # 清理测试目录
            print(f"\n清理测试目录: {test_dir}")
            shutil.rmtree(test_dir)
            print("✓ 测试目录已清理")
            
        else:
            print("✗ setup.py 运行失败或目录未创建")
            
    except Exception as e:
        print(f"\n测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        
        # 清理测试目录（如果存在）
        if test_dir.exists():
            shutil.rmtree(test_dir)
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    test_setup_workflow()