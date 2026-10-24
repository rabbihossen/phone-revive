# 📱 PhoneFix - Autonomous AI Android Health, Diagnostics & Performance Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Tests: 20 Passed](https://img.shields.io/badge/Tests-20%20Passed-success.svg)](tests/)
[![Android: 8.0 - 15+](https://img.shields.io/badge/Android-8.0%20--%2015%2B-orange.svg)](https://developer.android.com/)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Stdlib)-purple.svg)](requirements.txt)

> **PhoneFix** is an enterprise-grade, open-source Android diagnostics and performance optimization engine engineered for **humans and AI coding assistants** (Google Antigravity, Claude Code, Cursor, OpenHands).
>
> Simply point your AI agent or CLI to this repository, connect any Android phone via USB or Wi-Fi, and let PhoneFix audit system health, reclaim gigabytes of storage, eliminate RAM bottlenecks, disable ad bloatware, unlock 120Hz displays, and compile apps Ahead-of-Time — **with zero risk to personal photos, chats, or vault data**.

---

## 🌟 Why PhoneFix?

| Problem on Modern Android | Typical Solution | 🚀 The PhoneFix Advantage |
| :--- | :--- | :--- |
| **Intrusive Ad & Telemetry Daemons** (Xiaomi MSA, Samsung Free, Facebook Daemons) | Suspicious "Booster" PlayStore apps that add more ads | Safely uninstalls services for `user 0` without root. 100% reversible. |
| **High Refresh Rate Throttling** | Manually hunting obscure developer settings | Auto-detects 120Hz/90Hz hardware and unlocks peak refresh rate. |
| **App Launch Delays & JIT Stutter** | Restarting phone constantly | Runs native **Ahead-of-Time (AOT)** speed-profile bytecode compilation. |
| **In-App Pop-up Ads & Trackers** | Battery-draining VPN apps | Configures ultra-fast, zero-overhead Private DNS (e.g., KahfGuard / AdGuard). |
| **Data Safety & Fear of Bricking** | Risky custom recovery scripts | **Strict Safety First protocol**: Never touches user vaults (`.safebox`, `secretAlbum`, photos). |

---

## 🏗️ Architecture & Core Components

```
phone_fix/
├── core/                   # High-reliability ADB bridge, auto-discovery & device model
│   ├── adb.py              # USB & Wireless auto-discovery, shell wrappers & timeouts
│   ├── device.py           # Hardware specs, battery health, thermal & OS properties
│   └── exceptions.py       # Custom typed domain exceptions
├── analyzers/              # Non-destructive system diagnostics
│   ├── storage.py          # /data partitions, app caches, test APKs & junk files
│   ├── memory.py           # /proc/meminfo, dumpsys meminfo, ZRAM & swap pressure
│   ├── apps.py             # Dumpsys usagestats: active, inactive, and dormant apps
│   ├── display.py          # 60Hz/90Hz/120Hz refresh rates & animation scales
│   └── network.py          # Private DNS, IP discovery & security latency ping
├── brands/                 # Extensible Brand Strategy Pattern
│   ├── xiaomi.py           # MIUI & HyperOS (MSA, Analytics, Glance, Daemon, Joyose)
│   ├── samsung.py          # OneUI (Bixby, Samsung Free, GOS telemetry, Galaxy Store)
│   ├── realme_oppo_vivo.py # ColorOS, RealmeUI, FuntouchOS, OxygenOS
│   ├── pixel.py            # Google Pixel clean profile
│   └── generic.py          # Fallback for Motorola, Tecno, Infinix, etc.
├── engine/                 # Optimization & rollback orchestrator
│   ├── runner.py           # Diagnostic orchestrator & health scoring algorithm
│   └── optimizer.py        # Reversible bloatware removal, cache trim & AOT compilation
├── reports/                # Multi-format report generators
│   ├── markdown.py         # Structured GitHub-flavored markdown with benchmarks
│   └── console.py          # Portable zero-dependency ANSI terminal renderer
└── cli.py                  # Human and AI agent CLI interface
```

---

## ⚡ Quick Start for AI Agents (Claude / Antigravity / Cursor)

When interacting with an AI coding assistant, simply share this repository and say:
> *"Audit my connected Android phone, generate a health report, and wait for my confirmation before fixing anything."*

The AI assistant will strictly follow the [AGENTS.md](AGENTS.md) runbook:
1. **Check Connection:** Verifies device connection via `python3 -m phone_fix devices`.
2. **Audit & Report:** Runs non-destructive scan via `python3 -m phone_fix scan`.
3. **Present & Await Approval:** Explains findings, storage reclaimable, and asks for user confirmation.
4. **Execute & Benchmark:** Runs `python3 -m phone_fix optimize` and presents the before-and-after comparison.

---

## 💻 Manual CLI Usage

PhoneFix requires **no third-party Python packages** to run! It uses standard library Python 3.8+ and `adb`.

### 1. Check Attached Devices
```bash
python3 -m phone_fix devices
```

### 2. Connect via Wi-Fi (No Cable)
```bash
# For Android 11+ Wireless Debugging (First time pairing)
python3 -m phone_fix pair 192.168.0.100:39451 123456

# Connect to device
python3 -m phone_fix connect 192.168.0.100:5555
```

### 3. Run Non-Destructive Health Audit
```bash
python3 -m phone_fix scan --output device_health_report.md
```
*Outputs an ANSI terminal summary and writes a detailed markdown report.*

### 4. Optimize Device & Generate Benchmark
```bash
# Interactive mode (asks for confirmation)
python3 -m phone_fix optimize --output optimization_benchmark.md

# Automated mode (for AI agents or CI scripts)
python3 -m phone_fix optimize --yes --dns high.kahfguard.com
```

### 5. Rollback Packages (If Needed)
```bash
python3 -m phone_fix rollback com.miui.msa.global com.miui.analytics
```

---

## 🛡️ Safety & Privacy Guarantee

- **🔒 Zero Personal Data Loss:** Cache trimming uses Android's native `pm trim-caches`, which gracefully purges temporary HTTP and bitmap caches without logging you out of apps.
- **🚫 Vault Protection:** Encrypted private directories (like Xiaomi `.safebox` or `secretAlbum`) are strictly ignored and never modified.
- **↩️ 100% Reversible:** System bloatware is uninstalled only for `user 0` (`pm uninstall -k --user 0`). The base system APK remains untouched in the read-only system partition and can be re-enabled instantly with a single command.

---

## 🇧🇩 বাংলা নির্দেশিকা (Bengali Guide)

### কীভাবে ব্যবহার করবেন?
১. আপনার ফোনে **Developer Options** চালু করে **USB Debugging** (অথবা **Wireless Debugging**) অন করুন।  
২. ক্যাবল দিয়ে কানেক্ট করুন বা একই ওয়াইফাই নেটওয়ার্কে যুক্ত থাকুন।  
৩. টার্মিনালে বা আপনার AI অ্যাসিস্ট্যান্টকে বলুন:
```bash
python3 -m phone_fix scan
```
৪. সম্পূর্ণ ডায়াগনস্টিক রিপোর্ট দেখে আপনি সম্মতি দিলে অপ্টিমাইজেশন কার্যকর করুন:
```bash
python3 -m phone_fix optimize
```

---

## 🧪 Running Unit Tests

```bash
python3 -m pip install -r requirements-dev.txt
pytest -v
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
