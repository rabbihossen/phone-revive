"""
Terminal console renderer for PhoneFix.
Uses standard ANSI escape sequences for portable, zero-dependency styling.
"""

from phone_fix.engine.runner import HealthReport

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    GRAY = "\033[90m"

class ConsoleRenderer:
    """Renders formatted summaries directly into the terminal."""

    @staticmethod
    def print_header(title: str):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}  {title}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.RESET}\n")

    @staticmethod
    def print_report_summary(report: HealthReport):
        dev = report.device
        st = report.storage
        mem = report.memory
        apps = report.apps

        grade_color = Colors.GREEN if "A" in report.health_grade or "B" in report.health_grade else Colors.YELLOW
        if "D" in report.health_grade or "F" in report.health_grade:
            grade_color = Colors.RED

        print(f"📱 {Colors.BOLD}Device:{Colors.RESET} {dev.display_name} ({dev.model}) | Android {dev.android_version}")
        print(f"🔋 {Colors.BOLD}Battery:{Colors.RESET} {dev.battery.level}% ({dev.battery.health}) | Temp: {dev.battery.temperature_celsius}°C")
        print(f"🏆 {Colors.BOLD}Health Grade:{Colors.RESET} {grade_color}{report.health_grade}{Colors.RESET} (Score: {report.health_score}/100)")
        print(f"\n💾 {Colors.BOLD}Storage:{Colors.RESET} {st.free_gb:.1f} GB free of {st.total_gb:.1f} GB ({st.percent_used}% used)")
        print(f"   🧹 Cleanable Junk: {Colors.YELLOW}{st.total_cleanable_mb:.1f} MB{Colors.RESET}")
        print(f"\n🧠 {Colors.BOLD}Memory:{Colors.RESET} {mem.available_ram_mb:.0f} MB available of {mem.total_ram_mb:.0f} MB")
        print(f"   📊 Swap Load: {mem.swap_used_mb:.0f} MB / {mem.swap_total_mb:.0f} MB | Pressure: {mem.pressure_level}")

        if report.detected_bloatware:
            active_bloat = [b for b in report.detected_bloatware if not b.is_disabled]
            print(f"\n🛡️ {Colors.BOLD}Bloatware:{Colors.RESET} {len(active_bloat)} active / {len(report.detected_bloatware)} detected")

        if apps.dormant_apps:
            print(f"\n💤 {Colors.BOLD}Dormant Apps (>30 days):{Colors.RESET} {len(apps.dormant_apps)} apps")
            for a in apps.dormant_apps[:5]:
                print(f"   - {a.package_name} ({a.days_since_used} days ago)")

        if report.action_items:
            print(f"\n🎯 {Colors.BOLD}Recommended Action Items:{Colors.RESET}")
            for item in report.action_items:
                print(f"   {Colors.YELLOW}•{Colors.RESET} {item}")
        print("")
