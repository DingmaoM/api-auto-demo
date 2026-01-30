import subprocess
import sys
from datetime import datetime


def run_tests(report_type="allure"):
    """运行测试"""

    # 基本命令
    cmd = ["pytest"]

    # 生成报告
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if report_type == "allure":
        results_dir = f"./reports/allure-results-{timestamp}"
        cmd.extend(["--alluredir", results_dir])

    elif report_type == "html":
        report_file = f"./reports/test_report_{timestamp}.html"
        cmd.extend(["--html", report_file, "--self-contained-html"])

    # 运行测试
    print(f"运行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    # 生成Allure报告
    if report_type == "allure" and result.returncode == 0:
        report_dir = f"./reports/allure-report-{timestamp}"
        subprocess.run(["allure", "generate", results_dir, "-o", report_dir, "--clean"], shell=True)
        print(f"\nAllure报告已生成: {report_dir}")
        print(f"打开报告: allure open {report_dir}")
        # subprocess.run(["allure", "open", report_dir], shell=True)
    return result.returncode


if __name__ == "__main__":
    # 运行测试
    exit_code = run_tests()
    sys.exit(exit_code)

