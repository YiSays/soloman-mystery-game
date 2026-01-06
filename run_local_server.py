import os
import sys
import subprocess


def main():
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


if __name__ == "__main__":
    main()
