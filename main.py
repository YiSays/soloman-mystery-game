import shutil
import os
import sys
import filecmp
import subprocess
from pathlib import Path

# 配置路径
ROOT_DIR = Path(__file__).parent
WEBSITE_DIR = ROOT_DIR / "website"
DOCS_DIR = WEBSITE_DIR / "docs"

def needs_update(src: Path, dst: Path) -> bool:
    """
    检查文件是否需要更新。
    如果目标不存在，或者内容不同，返回 True。
    """
    if not dst.exists():
        return True
    # shallow=False 表示对比文件内容，不仅仅是元数据
    return not filecmp.cmp(src, dst, shallow=False)

def sync_files():
    """
    同步根目录 Markdown 文件到 website/docs，仅在有变更时操作。
    """
    print(f"🔄 正在检查文件变更...")
    
    updated_count = 0
    checked_count = 0

    # 1. 同步 Characters 文件夹
    src_chars = ROOT_DIR / "characters"
    dst_chars = DOCS_DIR / "characters"
    
    if src_chars.exists():
        dst_chars.mkdir(parents=True, exist_ok=True)
        for src_file in src_chars.glob("*.md"):
            dst_file = dst_chars / src_file.name
            checked_count += 1
            
            if needs_update(src_file, dst_file):
                shutil.copy2(src_file, dst_file)
                print(f"   📝 更新: characters/{src_file.name}")
                updated_count += 1
    
    # 2. 同步独立文件映射
    file_mapping = {
        "game_intro.md": "index.md",
        "dm_manual.md": "dm/manual.md",
        "clues_list.md": "dm/clues.md"
    }

    for src_name, dst_rel_path in file_mapping.items():
        src_file = ROOT_DIR / src_name
        dst_file = DOCS_DIR / dst_rel_path
        
        if src_file.exists():
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            checked_count += 1
            
            if needs_update(src_file, dst_file):
                shutil.copy2(src_file, dst_file)
                print(f"   📝 更新: {src_name} -> {dst_rel_path}")
                updated_count += 1
        else:
            print(f"   ⚠️ 警告: 源文件缺失 {src_name}")

    if updated_count == 0:
        print(f"   ✅ 所有文件 ({checked_count} 个) 均已是最新，无需同步。")
    else:
        print(f"   🎉 同步完成！共更新 {updated_count} 个文件。")

def run_server():
    """
    启动 MkDocs 预览服务器
    """
    print("\n🚀 准备启动 MkDocs 预览服务器...")
    print("   (按 Ctrl+C 停止服务)")
    print("-" * 50)
    
    try:
        # 在 website 目录下运行 mkdocs serve
        # check=False 允许我们处理非零退出码（尽管 serve 通常是持续运行的）
        subprocess.run(["mkdocs", "serve"], cwd=WEBSITE_DIR, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止。")
    except FileNotFoundError:
        print("\n❌ 错误: 未找到 'mkdocs' 命令。")
        print("   请确保您的虚拟环境中已安装: pip install mkdocs-material")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生意外错误: {e}")
        sys.exit(1)

def main():
    sync_files()
    run_server()

if __name__ == "__main__":
    main()
