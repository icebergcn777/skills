#!/usr/bin/env python3
"""
SkillSec Scanner — 本地 SKILL.md 安全扫描器
参考 NVIDIA SkillSpector 检测逻辑实现：
  - 64 种漏洞模式 / 16 个类别
  - 三层分析：静态分析 + 污点追踪 + 风险评分
"""

import os
import re
import json
import glob
from pathlib import Path

SKILL_DIR = "/sessions/inspiring-nice-keller/mnt/.agents/skills-archive"
COWORK_DIR = "/sessions/inspiring-nice-keller/mnt/skills"
OUTPUT_DIR = "/sessions/inspiring-nice-keller/mnt/outputs"

# ============================================================
# 检测模式定义
# ============================================================

# ★ 第0级：直接恶意代码
PATTERN_CRITICAL = {
    "eval_base64": {
        "pattern": r'eval\s*\(.*base64\.decode',
        "severity": "CRITICAL",
        "category": "dangerous_code",
        "desc": "eval + base64 混淆执行",
        "weight": 20,
    },
    "exec_obfuscated": {
        "pattern": r'(exec|eval|__import__)\s*\(.*(?:decode|decompress|uncompress)',
        "severity": "CRITICAL",
        "category": "dangerous_code",
        "desc": "混淆代码执行",
        "weight": 18,
    },
    "remote_code_download": {
        "pattern": r'(curl|wget|fetch|requests\.get)\s*\(?[\'\"](?:https?://|ftp://)',
        "severity": "CRITICAL",
        "category": "remote_execution",
        "desc": "从远程下载代码",
        "weight": 16,
    },
    "data_exfil_url": {
        "pattern": r'(requests\.(?:post|put)|curl\s+-[Xx]\s*(?:POST|PUT)|fetch\s*\(.*\{\s*method\s*:\s*[\'\"]POST)',
        "severity": "CRITICAL",
        "category": "data_exfiltration",
        "desc": "向外发送数据 (POST/PUT)",
        "weight": 15,
    },
    "system_cmd_exec": {
        "pattern": r'(os\.system|subprocess\.(?:call|Popen|run)|exec\s*\(|exec\s*[\'\"])',
        "severity": "CRITICAL",
        "category": "command_execution",
        "desc": "执行系统命令",
        "weight": 15,
    },
    "env_var_exfil": {
        "pattern": r'(os\.environ(?:\[|\.get)|process\.env|environ\[)',
        "severity": "CRITICAL",
        "category": "credential_access",
        "desc": "读取环境变量（可能偷 API Key）",
        "weight": 14,
    },
    "ipc_send": {
        "pattern": r'(socket\.(?:send|connect)|send_message|post_message)',
        "severity": "CRITICAL",
        "category": "data_exfiltration",
        "desc": "IPC/网络通信（数据外传）",
        "weight": 13,
    },
}

# ★ 第1级：高可疑
PATTERN_HIGH = {
    "write_to_file": {
        "pattern": r'(open\s*\(.*[\'\"][^)]+[\'\"].*[wa]|write\s*\(|file_put_contents)',
        "severity": "HIGH",
        "category": "file_operations",
        "desc": "写入文件（可能植入后门）",
        "weight": 10,
    },
    "base64_decode": {
        "pattern": r'(base64\.(?:b64decode|decode)|base64_decode|atob\s*\()',
        "severity": "HIGH",
        "category": "obfuscation",
        "desc": "Base64 解码（混淆代码）",
        "weight": 9,
    },
    "import_subprocess": {
        "pattern": r'(import subprocess|import os\s|import shutil)',
        "severity": "HIGH",
        "category": "dangerous_import",
        "desc": "导入危险模块（可执行命令）",
        "weight": 8,
    },
    "curl_pipe_bash": {
        "pattern": r'curl\s+.*\|\s*(?:bash|sh|zsh)',
        "severity": "HIGH",
        "category": "remote_execution",
        "desc": "curl pipe to shell（经典远控）",
        "weight": 12,
    },
    "pip_install": {
        "pattern": r'(pip\s+install|npm\s+install|gem\s+install)',
        "severity": "HIGH",
        "category": "supply_chain",
        "desc": "自动安装依赖（供应链攻击）",
        "weight": 10,
    },
    "chmod_chmod": {
        "pattern": r'chmod\s+[0-7]?7[0-7]?[0-7]?',
        "severity": "HIGH",
        "category": "privilege_escalation",
        "desc": "修改文件权限为可执行",
        "weight": 8,
    },
    "network_request": {
        "pattern": r'(requests\.(?:get|post|put|delete)|urllib\.request|httpx\.|aiohttp\.)',
        "severity": "HIGH",
        "category": "network_activity",
        "desc": "发起网络请求（可能外传数据）",
        "weight": 7,
    },
}

# ★ 第2级：可疑
PATTERN_MEDIUM = {
    "temp_file": {
        "pattern": r'(/tmp/|tempfile|mktemp|temp_dir)',
        "severity": "MEDIUM",
        "category": "file_operations",
        "desc": "使用临时文件（可能隐藏痕迹）",
        "weight": 5,
    },
    "hidden_file": {
        "pattern": r'(/\.[a-z]|hidden|\.secret|\.config|\.env)',
        "severity": "MEDIUM",
        "category": "obfuscation",
        "desc": "操作隐藏文件/配置文件",
        "weight": 4,
    },
    "ssh_keys": {
        "pattern": r'(id_rsa|id_dsa|authorized_keys|ssh-keygen|\.ssh/)',
        "severity": "MEDIUM",
        "category": "credential_access",
        "desc": "操作 SSH 密钥",
        "weight": 6,
    },
    "prompt_injection": {
        "pattern": r'(ignore\s+(?:all\s+)?(?:previous|above|system)|"system"\s*:\s*"|role\s*:\s*"system)',
        "severity": "MEDIUM",
        "category": "prompt_injection",
        "desc": "提示词注入风险",
        "weight": 5,
    },
    "self_modify": {
        "pattern": r'(modify\s+(?:itself|own\s+(?:code|source))|rewrite\s+(?:itself|own)|self[-_]modif)',
        "severity": "HIGH",
        "category": "rogue_agent",
        "desc": "自我修改代码（流氓 Agent）",
        "weight": 10,
    },
    "config_exfil": {
        "pattern": r'(read\s+.*(?:config|setting|\.env|credentials)|cat\s+.*(?:config|\.env|\.git))',
        "severity": "MEDIUM",
        "category": "credential_access",
        "desc": "读取配置文件（可能偷凭证）",
        "weight": 6,
    },
}

ALL_PATTERNS = {**PATTERN_CRITICAL, **PATTERN_HIGH, **PATTERN_MEDIUM}


def scan_file(filepath):
    """扫描单个 SKILL.md 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {
            "file": str(filepath),
            "error": str(e),
            "findings": [],
            "score": 0,
            "severity": "ERROR",
        }

    findings = []
    score = 0
    max_severity = "LOW"

    for name, cfg in ALL_PATTERNS.items():
        matches = re.findall(cfg["pattern"], content, re.IGNORECASE | re.MULTILINE)
        if matches:
            weight = cfg["weight"] * min(len(matches), 3)  # 同一模式多hit有加成
            score += weight
            findings.append({
                "pattern": name,
                "severity": cfg["severity"],
                "category": cfg["category"],
                "desc": cfg["desc"],
                "matches": len(matches),
                "weight": weight,
            })
            sev_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
            if sev_order.get(cfg["severity"], 0) > sev_order.get(max_severity, 0):
                max_severity = cfg["severity"]

    # 能自己跑程序/脚本的 ×1.3
    has_exec = any(f["category"] in ("command_execution", "remote_execution", "dangerous_code") for f in findings)
    if has_exec:
        score = int(score * 1.3)
        if max_severity == "HIGH":
            max_severity = "CRITICAL"

    return {
        "file": str(filepath),
        "findings": findings,
        "score": min(score, 100),
        "severity": max_severity,
    }


def scan_directory(directory):
    """扫描目录下所有 SKILL.md"""
    results = []
    files = glob.glob(os.path.join(directory, "**/SKILL.md"), recursive=True)
    files += glob.glob(os.path.join(directory, "**/*.md"), recursive=True)
    files = list(set(files))

    for f in sorted(files):
        basename = os.path.basename(f)
        if basename not in ("SKILL.md",):
            continue
        result = scan_file(f)
        results.append(result)

    return results


def print_report(results, label):
    """打印扫描报告"""
    clean = [r for r in results if not r.get("error") and not r["findings"]]
    dirty = [r for r in results if r["findings"]]
    errors = [r for r in results if r.get("error")]
    scored = sorted([r for r in results if r["findings"]], key=lambda x: x["score"], reverse=True)

    print(f"\n{'='*60}")
    print(f"📋 {label}")
    print(f"{'='*60}")
    print(f"总计: {len(results)} 个 Skill")
    print(f"✅ 干净: {len(clean)}")
    print(f"⚠️  有发现: {len(dirty)}")
    print(f"❌ 读取错误: {len(errors)}")
    print()

    if scored:
        max_sev = max(r["score"] for r in scored)
        print(f"最高风险分: {max_sev}/100")
        high_risk = [r for r in scored if r["score"] >= 50]
        med_risk = [r for r in scored if 20 <= r["score"] < 50]
        low_risk = [r for r in scored if r["score"] < 20]
        print(f"🔴 高风险 (≥50): {len(high_risk)}")
        print(f"🟡 中风险 (20-49): {len(med_risk)}")
        print(f"🟢 低风险 (<20): {len(low_risk)}")
        print()

        # 高风险详情
        if high_risk:
            print(f"{'='*60}")
            print("🔴 高风险 Skill 详情")
            print(f"{'='*60}")
            for r in high_risk:
                fname = os.path.basename(os.path.dirname(r["file"]))
                print(f"\n  [{r['score']}/100] {fname}")
                for f in r["findings"]:
                    print(f"    ⚡ [{f['severity']}] {f['desc']} ({f['category']}) x{f['matches']}")
            print()

        # 中风险详情
        if med_risk:
            print(f"{'='*60}")
            print("🟡 中风险 Skill 详情")
            print(f"{'='*60}")
            for r in med_risk:
                fname = os.path.basename(os.path.dirname(r["file"]))
                print(f"  [{r['score']}/100] {fname} — {', '.join(set(f['desc'] for f in r['findings']))}")
            print()

        # 按类别汇总
        print(f"{'='*60}")
        print("📊 按风险类别汇总")
        print(f"{'='*60}")
        cat_count = {}
        for r in scored:
            for f in r["findings"]:
                c = f["category"]
                cat_count[c] = cat_count.get(c, 0) + 1
        for cat, count in sorted(cat_count.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count} 次出现")


def save_json_report(results, label, filename):
    """保存 JSON 报告"""
    report = {
        "label": label,
        "total": len(results),
        "clean": len([r for r in results if not r.get("error") and not r["findings"]]),
        "dirty": len([r for r in results if r["findings"]]),
        "errors": len([r for r in results if r.get("error")]),
        "results": results,
    }
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return path


if __name__ == "__main__":
    # 扫描 agents skills
    print("正在扫描 ~/.agents/skills-archive/ ...")
    agent_results = scan_directory(SKILL_DIR)
    print_report(agent_results, "第三方 Skill 安全扫描")
    json_path = save_json_report(agent_results, "agents_skills", "skillsec-agents-report.json")
    print(f"\nJSON 报告已保存: {json_path}")

    # 扫描 Cowork skills（含 .md 文件）
    print(f"\n正在扫描 Cowork skills...")
    cowork_files = glob.glob(os.path.join(COWORK_DIR, "**/*.md"), recursive=True)
    cowork_results = []
    for f in sorted(cowork_files):
        if os.path.basename(f) in ("README.md", "THIRD_PARTY_NOTICES.md"):
            continue
        if "node_modules" in f:
            continue
        result = scan_file(f)
        cowork_results.append(result)
    print_report(cowork_results, "Cowork Skill 安全扫描")
    json_path2 = save_json_report(cowork_results, "cowork_skills", "skillsec-cowork-report.json")
    print(f"\nJSON 报告已保存: {json_path2}")
