"""
Command Line Interface (CLI) for PhoneFix.
Provides accessible, intuitive commands for users, scripts, and AI coding agents.
"""

import argparse
import sys
from typing import List, Optional

from phone_fix.core.adb import AdbBridge
from phone_fix.core.exceptions import PhoneFixError
from phone_fix.engine.runner import DiagnosticRunner
from phone_fix.engine.optimizer import DeviceOptimizer
from phone_fix.reports.console import ConsoleRenderer, Colors
from phone_fix.reports.markdown import MarkdownReportGenerator

def create_parser() -> argparse.ArgumentParser:
    common_parent = argparse.ArgumentParser(add_help=False)
    common_parent.add_argument("--serial", "-s", help="Target specific device serial or IP:port")

    parser = argparse.ArgumentParser(
        prog="phone-fix",
        parents=[common_parent],
        description="PhoneFix: Autonomous AI-Powered Android Health, Diagnostics & Performance Optimizer."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # scan
    scan_p = subparsers.add_parser("scan", parents=[common_parent], help="Run comprehensive non-destructive diagnostics")
    scan_p.add_argument("--output", "-o", default="device_health_report.md", help="Markdown report output path")
    scan_p.add_argument("--json", action="store_true", help="Output raw JSON data")

    # optimize
    opt_p = subparsers.add_parser("optimize", parents=[common_parent], help="Safely execute proposed optimizations and benchmark")
    opt_p.add_argument("--output", "-o", default="optimization_benchmark.md", help="Markdown benchmark output path")
    opt_p.add_argument("--dns", default="high.kahfguard.com", help="Private DNS hostname for ad-blocking")
    opt_p.add_argument("--no-dns", action="store_true", help="Skip Private DNS configuration")
    opt_p.add_argument("--yes", "-y", action="store_true", help="Skip interactive confirmation")

    # rollback
    rb_p = subparsers.add_parser("rollback", parents=[common_parent], help="Restore uninstalled packages for user 0")
    rb_p.add_argument("packages", nargs="+", help="Package names to restore")

    # devices
    subparsers.add_parser("devices", help="List all attached ADB devices and their authorization status")

    # connect
    conn_p = subparsers.add_parser("connect", help="Connect to device over Wi-Fi")
    conn_p.add_argument("address", help="Device IP and port (e.g. 192.168.0.100:5555)")

    # pair
    pair_p = subparsers.add_parser("pair", help="Pair device over wireless debugging (Android 11+)")
    pair_p.add_argument("address", help="Device IP and port (e.g. 192.168.0.100:39451)")
    pair_p.add_argument("code", help="6-digit Wi-Fi pairing code")

    return parser

def cmd_devices(adb: AdbBridge):
    devices = adb.list_devices()
    ConsoleRenderer.print_header("Connected Android Devices")
    if not devices:
        print(f"{Colors.YELLOW}No devices detected.{Colors.RESET}")
        print("Please enable Developer Options -> USB Debugging on your phone.")
        return

    for d in devices:
        status_col = Colors.GREEN if d.is_authorized else Colors.RED
        print(f"• {Colors.BOLD}{d.serial}{Colors.RESET} [{status_col}{d.state}{Colors.RESET}] - Model: {d.model or 'Unknown'}")
    print("")

def cmd_scan(adb: AdbBridge, output_path: str, output_json: bool):
    dev = adb.select_device(adb.target_serial)
    ConsoleRenderer.print_header(f"Scanning Device: {dev.serial}")
    runner = DiagnosticRunner(adb)
    report = runner.run()

    ConsoleRenderer.print_report_summary(report)

    md_content = MarkdownReportGenerator.generate(report)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"📄 Detailed report saved to: {Colors.CYAN}{output_path}{Colors.RESET}\n")

def cmd_optimize(adb: AdbBridge, output_path: str, dns_host: str, skip_dns: bool, auto_yes: bool):
    dev = adb.select_device(adb.target_serial)
    ConsoleRenderer.print_header(f"Optimizing Device: {dev.serial}")

    # 1. Capture before metrics
    print(f"🔍 Running pre-optimization baseline diagnostics...")
    runner = DiagnosticRunner(adb)
    before_report = runner.run()

    if not auto_yes:
        print(f"{Colors.BOLD}Target optimizations:{Colors.RESET}")
        print(f"  1. Trim app caches (Safe system-level eviction)")
        print(f"  2. Remove leftover test APKs and gallery thumbnails (~{before_report.storage.removable_tmp_bytes / (1024*1024):.0f} MB)")
        print(f"  3. Disable detected telemetry & ad bloatware ({len(before_report.detected_bloatware)} items)")
        print(f"  4. Set display refresh rate to 120Hz & UI animation scale to 0.5x")
        print(f"  5. Compile primary active apps (AOT speed-profile)")
        if not skip_dns:
            print(f"  6. Configure ad-blocking Private DNS ({dns_host})")

        confirm = input(f"\n{Colors.YELLOW}Proceed with optimization? [Y/n]: {Colors.RESET}").strip().lower()
        if confirm and confirm != "y":
            print("Optimization aborted by user.")
            return

    optimizer = DeviceOptimizer(adb)

    # 1. Trim caches
    print(f"\n[1/6] 🧹 Trimming application caches...")
    optimizer.trim_caches()

    # 2. Clean tmp files
    print(f"[2/6] 🗑️ Cleaning leftover temporary files and thumbnails...")
    optimizer.clean_tmp_junk()

    # 3. Disable bloatware
    active_bloat = [b.package_name for b in before_report.detected_bloatware if not b.is_disabled]
    if active_bloat:
        print(f"[3/6] 🛡️ Disabling {len(active_bloat)} telemetry/ad bloatware packages...")
        disabled, failed = optimizer.disable_bloatware(active_bloat)
        print(f"       Successfully disabled: {len(disabled)} packages")

    # 4. Refresh rate and animation
    print(f"[4/6] ⚡ Unlocking 120Hz refresh rate & 0.5x animation scales...")
    optimizer.unlock_refresh_rate(120)
    optimizer.optimize_animations(0.5)

    # 5. AOT DEX Compilation for active apps
    primary_apps = [
        "com.miui.home",
        "com.android.systemui",
        "com.facebook.katana",
        "com.whatsapp",
        "com.android.chrome",
        "com.facebook.orca"
    ]
    print(f"[5/6] 🚀 Running Ahead-of-Time (AOT) speed-profile compilation...")
    optimizer.compile_apps_aot(primary_apps)

    # Standby bucket for dormant apps
    dormant_pkgs = [a.package_name for a in before_report.apps.dormant_apps]
    if dormant_pkgs:
        optimizer.restrict_dormant_apps(dormant_pkgs)

    # 6. DNS
    if not skip_dns and dns_host:
        print(f"[6/6] 🌐 Configuring Private DNS ({dns_host})...")
        optimizer.set_private_dns(dns_host)

    # Kill cached to apply
    optimizer.kill_cached_processes()

    # 7. Post-optimization metrics
    print(f"\n🔍 Running post-optimization verification...")
    after_report = runner.run()

    ConsoleRenderer.print_report_summary(after_report)

    benchmark_md = MarkdownReportGenerator.generate(after_report, before_report=before_report)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(benchmark_md)

    print(f"🎉 Optimization complete! Benchmark report saved to: {Colors.CYAN}{output_path}{Colors.RESET}\n")

def cmd_rollback(adb: AdbBridge, packages: List[str]):
    dev = adb.select_device(adb.target_serial)
    ConsoleRenderer.print_header(f"Rolling Back Packages on {dev.serial}")
    optimizer = DeviceOptimizer(adb)
    restored = optimizer.rollback_packages(packages)
    print(f"Successfully restored {len(restored)} / {len(packages)} packages.")
    for p in restored:
        print(f"  • {p}")

def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        adb = AdbBridge(target_serial=args.serial)

        if args.command == "devices":
            cmd_devices(adb)
        elif args.command == "scan":
            cmd_scan(adb, args.output, args.json)
        elif args.command == "optimize":
            cmd_optimize(adb, args.output, args.dns, args.no_dns, args.yes)
        elif args.command == "rollback":
            cmd_rollback(adb, args.packages)
        elif args.command == "connect":
            res = adb.connect_wifi(args.address)
            print(res)
        elif args.command == "pair":
            res = adb.pair_wifi(args.address, args.code)
            print(res)

    except PhoneFixError as e:
        print(f"\n{Colors.RED}Error:{Colors.RESET} {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected Error:{Colors.RESET} {e}\n", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
