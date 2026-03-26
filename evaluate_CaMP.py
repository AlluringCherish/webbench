#!/usr/bin/env python3

import os
import sys
import json
import shutil
import subprocess
import signal
import time
import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import select
import termios
import tty

SCRIPT_DIR = Path(__file__).resolve().parent

APP_TYPE_CONFIGS = {
    'web': {
        'name': 'Web Applications',
        'display_name': 'Software-web',
        'base_path': str(SCRIPT_DIR / 'results'),
        'folder_prefix': 'Software-web',
        'testcode_dir': str(SCRIPT_DIR / 'benchmark' / 'Software' / 'web' / 'testcode'),
        'test_script_pattern': 'Test{task}_wsl.py',
        'test_data_base': str(SCRIPT_DIR / 'benchmark' / 'Software' / 'web' / 'data'),
        'requires_server': True,
        'server_port': 5000,
        'requires_data_injection': True,
        'entry_file': 'app.py',
        'test_timeout': 300,
        'framework': 'Flask + Selenium'
    },
    'gui': {
        'name': 'GUI Applications',
        'display_name': 'Software-gui',
        'base_path': str(SCRIPT_DIR / 'results'),
        'folder_prefix': 'Software-gui',
        'testcode_dir': str(SCRIPT_DIR / 'benchmark' / 'Software' / 'gui' / 'testcode'),
        'test_script_pattern': 'Test{task}.py',
        'test_data_base': None,
        'requires_server': False,
        'server_port': None,
        'requires_data_injection': False,
        'entry_file': 'app.py',
        'test_timeout': 300,
        'framework': 'Tkinter + unittest'
    },
    'gaia': {
        'name': 'GAIA Benchmark',
        'display_name': 'GAIA',
        'base_path': str(SCRIPT_DIR / 'results'),
        'benchmark_path': str(SCRIPT_DIR / 'benchmark' / 'GAIA' / 'validation'),
        'requires_server': False,
        'requires_data_injection': False,
        'framework': 'Question Answering'
    },
    'gpqa': {
        'name': 'GPQA-Diamond Benchmark',
        'display_name': 'GPQA_Diamond',
        'base_path': str(SCRIPT_DIR / 'results'),
        'benchmark_path': str(SCRIPT_DIR / 'benchmark' / 'GPQA_Diamond'),
        'requires_server': False,
        'requires_data_injection': False,
        'framework': 'Multiple Choice QA'
    }
}

CURRENT_CONFIG = None

_skip_requested = False
_original_terminal_settings = None
_key_listener_thread = None
_key_listener_active = False

AVAILABLE_SCENARIOS = ["vanilla", "agent_chaos", "stress_chaos", "io_chaos", "complex_chaos", "compound_chaos", "compound"]

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")


def print_success(text: str):
    print(f"{Colors.OKGREEN}{text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.FAIL}{text}{Colors.ENDC}")


def print_warning(text: str):
    print(f"{Colors.WARNING}{text}{Colors.ENDC}")


def print_info(text: str):
    print(f"{Colors.OKCYAN}{text}{Colors.ENDC}")


def print_skip(text: str):
    print(f"{Colors.WARNING}[SKIP] {text}{Colors.ENDC}")


def setup_terminal():
    global _original_terminal_settings
    try:
        _original_terminal_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
    except:
        pass


def restore_terminal():
    global _original_terminal_settings
    if _original_terminal_settings:
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _original_terminal_settings)
        except:
            pass


def _key_listener_worker():
    global _skip_requested, _key_listener_active
    while _key_listener_active:
        try:
            if select.select([sys.stdin], [], [], 0.1)[0]:
                key = sys.stdin.read(1)
                if key.lower() == 's':
                    _skip_requested = True
        except:
            pass


def start_key_listener():
    global _key_listener_thread, _key_listener_active
    _key_listener_active = True
    _key_listener_thread = threading.Thread(target=_key_listener_worker, daemon=True)
    _key_listener_thread.start()


def stop_key_listener():
    global _key_listener_thread, _key_listener_active
    _key_listener_active = False
    if _key_listener_thread:
        _key_listener_thread.join(timeout=0.5)
        _key_listener_thread = None


def reset_skip_flag():
    global _skip_requested
    _skip_requested = False


def select_app_type() -> dict:
    print_header("Select Evaluation Type")

    print("\nAvailable evaluation types:")
    print(f"  [1] {APP_TYPE_CONFIGS['web']['name']} ({APP_TYPE_CONFIGS['web']['framework']})")
    print(f"  [2] {APP_TYPE_CONFIGS['gui']['name']} ({APP_TYPE_CONFIGS['gui']['framework']})")
    print(f"  [3] {APP_TYPE_CONFIGS['gaia']['name']} ({APP_TYPE_CONFIGS['gaia']['framework']})")
    print(f"  [4] {APP_TYPE_CONFIGS['gpqa']['name']} ({APP_TYPE_CONFIGS['gpqa']['framework']})")

    while True:
        choice = input(f"\n{Colors.OKBLUE}Select type (1-4): {Colors.ENDC}").strip()

        if choice == '1':
            selected_config = APP_TYPE_CONFIGS['web']
            break
        elif choice == '2':
            selected_config = APP_TYPE_CONFIGS['gui']
            break
        elif choice == '3':
            selected_config = APP_TYPE_CONFIGS['gaia']
            break
        elif choice == '4':
            selected_config = APP_TYPE_CONFIGS['gpqa']
            break
        else:
            print_error("Invalid selection. Please select 1, 2, 3, or 4.")

    print_success(f"Selected: {selected_config['name']}")
    print_info(f"Framework: {selected_config['framework']}\n")

    return selected_config


def normalize_number_str(number_str: str) -> float:
    for char in ["$", "%", ","]:
        number_str = number_str.replace(char, "")
    try:
        return float(number_str)
    except ValueError:
        return float("inf")


def split_string(s: str, char_list: list = [",", ";"]) -> list:
    pattern = f"[{''.join(char_list)}]"
    return re.split(pattern, s)


def normalize_str(input_str: str, remove_punct: bool = True) -> str:
    import string
    no_spaces = re.sub(r"\s", "", input_str)
    if remove_punct:
        translator = str.maketrans("", "", string.punctuation)
        return no_spaces.lower().translate(translator)
    else:
        return no_spaces.lower()


def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def select_gaia_benchmark_folder(config: dict) -> Optional[Path]:
    base_path = Path(config['base_path'])
    gaia_folders = sorted([
        f for f in base_path.iterdir()
        if f.is_dir() and f.name.startswith("GAIA-")
    ])

    if not gaia_folders:
        print_error("No GAIA benchmark folders found in results/")
        return None

    print_header("Select GAIA Benchmark Folder")
    for i, folder in enumerate(gaia_folders, 1):
        print(f"  [{i}] {folder.name}")

    while True:
        try:
            choice = input(f"\n{Colors.OKBLUE}Select folder (1-{len(gaia_folders)}, or 'q' to quit): {Colors.ENDC}").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(gaia_folders):
                selected = gaia_folders[idx]
                print_success(f"Selected: {selected.name}")
                return selected
            print_error("Invalid selection. Try again.")
        except ValueError:
            print_error("Please enter a valid number.")


def select_gaia_timestamp(benchmark_path: Path) -> Optional[Path]:
    timestamp_folders = sorted([
        f for f in benchmark_path.iterdir()
        if f.is_dir() and f.name[0].isdigit()
    ])

    if not timestamp_folders:
        print_error(f"No timestamp folders found in {benchmark_path.name}/")
        return None

    print_header("Select Timestamp")
    for i, folder in enumerate(timestamp_folders, 1):
        task_count = len([f for f in folder.iterdir() if f.is_dir()])
        print(f"  [{i}] {folder.name} ({task_count} tasks)")

    while True:
        try:
            choice = input(f"\n{Colors.OKBLUE}Select timestamp (1-{len(timestamp_folders)}, or 'q' to quit): {Colors.ENDC}").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(timestamp_folders):
                selected = timestamp_folders[idx]
                print_success(f"Selected: {selected.name}")
                return selected
            print_error("Invalid selection. Try again.")
        except ValueError:
            print_error("Please enter a valid number.")


def select_gaia_scenario() -> Optional[List[str]]:
    print_header("Select Scenario")
    print("  [0] all (evaluate all scenarios)")
    for i, scenario in enumerate(AVAILABLE_SCENARIOS, 1):
        print(f"  [{i}] {scenario}")

    while True:
        try:
            choice = input(f"\n{Colors.OKBLUE}Select scenario (0-{len(AVAILABLE_SCENARIOS)}, or 'q' to quit): {Colors.ENDC}").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice)
            if idx == 0:
                return AVAILABLE_SCENARIOS
            elif 1 <= idx <= len(AVAILABLE_SCENARIOS):
                return [AVAILABLE_SCENARIOS[idx - 1]]
            print_error("Invalid selection. Try again.")
        except ValueError:
            print_error("Please enter a valid number.")


def get_gaia_metadata_path(benchmark_name: str, config: dict) -> Path:
    folder_name = benchmark_name.replace("GAIA-", "")
    return Path(config['benchmark_path']) / folder_name / "metadata.jsonl"


def load_gaia_metadata(benchmark_name: str, config: dict) -> Dict[str, dict]:
    metadata_path = get_gaia_metadata_path(benchmark_name, config)

    if not metadata_path.exists():
        print_warning(f"Metadata file not found: {metadata_path}")
        return {}

    metadata = {}
    with open(metadata_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                entry = json.loads(line)
                task_id = entry.get("task_id")
                if task_id:
                    metadata[task_id] = entry

    return metadata


def parse_gaia_final_answer(file_path: Path) -> Optional[str]:
    if not file_path.exists():
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            return ""

        prefix_pattern = r'(?i)final\s*answer\s*:\s*'
        match = re.search(prefix_pattern, content)

        if match:
            answer = content[match.end():].strip()
        else:
            answer = content

        trailing_patterns = [
            r'\s*\[APPROVED\]\s*$',
            r'\s*\[VERIFIED\]\s*$',
            r'\s*\[CONFIRMED\]\s*$',
        ]
        for pattern in trailing_patterns:
            answer = re.sub(pattern, '', answer, flags=re.IGNORECASE).strip()

        return answer

    except Exception as e:
        print_warning(f"Error reading {file_path}: {e}")
        return None


def compare_gaia_answers(predicted: str, ground_truth: str) -> bool:
    if predicted is None:
        predicted = "None"

    if is_float(ground_truth):
        normalized_answer = normalize_number_str(predicted)
        return normalized_answer == float(ground_truth)

    elif any(char in ground_truth for char in [",", ";"]):
        gt_elems = split_string(ground_truth)
        ma_elems = split_string(predicted)

        if len(gt_elems) != len(ma_elems):
            return False

        comparisons = []
        for ma_elem, gt_elem in zip(ma_elems, gt_elems):
            if is_float(gt_elem):
                normalized_ma_elem = normalize_number_str(ma_elem)
                comparisons.append(normalized_ma_elem == float(gt_elem))
            else:
                comparisons.append(
                    normalize_str(ma_elem, remove_punct=False)
                    == normalize_str(gt_elem, remove_punct=False)
                )
        return all(comparisons)

    else:
        return normalize_str(predicted) == normalize_str(ground_truth)


def load_gaia_task_metrics(scenario_path: Path) -> dict:
    metrics_path = scenario_path / "metrics.json"
    default_metrics = {
        "duration_seconds": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "model": "unknown",
        "status": "unknown"
    }

    if not metrics_path.exists():
        return default_metrics

    try:
        with open(metrics_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        duration = data.get("task_duration", 0)

        input_tokens = 0
        output_tokens = 0
        model_name = "unknown"

        by_model = data.get("by_model", {})
        if by_model:
            model_name = list(by_model.keys())[0]
            model_data = by_model[model_name]
            input_tokens = model_data.get("prompt_tokens", 0)
            output_tokens = model_data.get("completion_tokens", 0)

        final_answer_path = scenario_path / "final_answer.txt"
        status = "success" if final_answer_path.exists() else "failed"

        return {
            "duration_seconds": duration,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "model": model_name,
            "status": status
        }
    except Exception as e:
        print_warning(f"Error reading metrics from {metrics_path}: {e}")
        return default_metrics


def evaluate_gaia_scenario(
    timestamp_path: Path,
    scenario: str,
    metadata: Dict[str, dict]
) -> Tuple[List[dict], List[str], Dict[str, dict]]:
    answers = []
    missing_tasks = []
    results = {}

    task_folders = [f for f in timestamp_path.iterdir() if f.is_dir() and '-' in f.name]

    for task_folder in sorted(task_folders):
        task_id = task_folder.name
        scenario_path = task_folder / scenario

        if not scenario_path.exists():
            continue

        final_answer_path = scenario_path / "final_answer.txt"
        predicted_answer = parse_gaia_final_answer(final_answer_path)

        task_meta = metadata.get(task_id, {})
        question = task_meta.get("Question", "")
        level = task_meta.get("Level", 0)
        ground_truth = task_meta.get("Final answer", "")

        metrics = load_gaia_task_metrics(scenario_path)

        if predicted_answer is None:
            missing_tasks.append(task_id)
            predicted_answer = ""
            is_correct = False
            status = "failed"
        else:
            is_correct = compare_gaia_answers(predicted_answer, ground_truth) if ground_truth else False
            status = metrics["status"]

        answer_entry = {
            "task_id": task_id,
            "Question": question,
            "Level": level,
            "Final answer": predicted_answer
        }
        answers.append(answer_entry)

        results[task_id] = {
            "predicted": predicted_answer,
            "ground_truth": ground_truth,
            "level": level,
            "correct": is_correct,
            "status": status,
            "duration_seconds": metrics["duration_seconds"],
            "input_tokens": metrics["input_tokens"],
            "output_tokens": metrics["output_tokens"],
            "model": metrics["model"]
        }

    return answers, missing_tasks, results


def save_gaia_answers_jsonl(timestamp_path: Path, scenario: str, answers: List[dict]) -> Path:
    output_path = timestamp_path / f"{scenario}_answers.jsonl"

    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in answers:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    return output_path


def calculate_gaia_summary(
    timestamp_path: Path,
    scenario: str,
    results: Dict[str, dict],
    benchmark_name: str
) -> dict:
    if not results:
        return {}

    timestamp = timestamp_path.name

    model = "unknown"
    for r in results.values():
        if r.get("model") and r.get("model") != "unknown":
            model = r["model"]
            break

    total = len(results)
    correct = sum(1 for r in results.values() if r["correct"])
    accuracy = (correct / total * 100) if total > 0 else 0

    total_input_tokens = sum(r.get("input_tokens", 0) for r in results.values())
    total_output_tokens = sum(r.get("output_tokens", 0) for r in results.values())
    total_duration = sum(r.get("duration_seconds", 0) for r in results.values())

    level_stats = {}
    for task_id, result in results.items():
        level = result.get("level", 0)
        if level not in level_stats:
            level_stats[level] = {
                "total": 0,
                "correct": 0,
                "total_tokens": 0,
                "total_time": 0
            }
        level_stats[level]["total"] += 1
        level_stats[level]["total_tokens"] += result.get("input_tokens", 0) + result.get("output_tokens", 0)
        level_stats[level]["total_time"] += result.get("duration_seconds", 0)
        if result["correct"]:
            level_stats[level]["correct"] += 1

    for level in level_stats:
        stats = level_stats[level]
        stats["accuracy"] = round(stats["correct"] / stats["total"] * 100, 2) if stats["total"] > 0 else 0
        stats["avg_tokens"] = round(stats["total_tokens"] / stats["total"]) if stats["total"] > 0 else 0
        stats["avg_time"] = round(stats["total_time"] / stats["total"], 2) if stats["total"] > 0 else 0
        del stats["total_tokens"]
        del stats["total_time"]

    results_array = []
    for task_id, result in sorted(results.items()):
        results_array.append({
            "task_id": task_id,
            "level": result.get("level", 0),
            "correct": result["correct"],
            "status": result.get("status", "unknown"),
            "predicted": result["predicted"],
            "ground_truth": result["ground_truth"],
            "tokens": result.get("input_tokens", 0) + result.get("output_tokens", 0),
            "duration_seconds": result.get("duration_seconds", 0)
        })

    summary = {
        "timestamp": timestamp,
        "model": model,
        "benchmark": benchmark_name,
        "scenario": scenario,
        "total_duration_seconds": round(total_duration, 2),
        "statistics": {
            "total": total,
            "correct": correct,
            "accuracy": round(accuracy, 2),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "avg_tokens": round((total_input_tokens + total_output_tokens) / total) if total > 0 else 0,
            "avg_time": round(total_duration / total, 2) if total > 0 else 0
        },
        "level_statistics": level_stats,
        "results": results_array
    }

    return summary


def save_gaia_summary(timestamp_path: Path, scenario: str, summary: dict) -> Path:
    output_path = timestamp_path / f"{scenario}_summary.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return output_path


def print_gaia_results(
    scenario: str,
    results: Dict[str, dict],
    missing_tasks: List[str],
    jsonl_path: Path
):
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario}")
    print(f"{'='*60}")

    if missing_tasks:
        print(f"\n{Colors.WARNING}=== Failed Tasks (no final_answer.txt) ==={Colors.ENDC}")
        for task_id in sorted(missing_tasks):
            print(f"  - {task_id}")
        print(f"Total missing: {len(missing_tasks)}")

    if not results:
        print_warning("No results to evaluate.")
        return

    total_correct = sum(1 for r in results.values() if r["correct"])
    total_count = len(results)

    level_stats = {}
    for task_id, result in results.items():
        level = result["level"]
        if level not in level_stats:
            level_stats[level] = {"correct": 0, "total": 0}
        level_stats[level]["total"] += 1
        if result["correct"]:
            level_stats[level]["correct"] += 1

    print(f"\n{Colors.BOLD}=== Evaluation Results ==={Colors.ENDC}")
    print_info(f"JSONL saved: {jsonl_path}")
    print(f"\n{Colors.BOLD}Overall: {total_correct}/{total_count} ({100*total_correct/total_count:.2f}%){Colors.ENDC}")

    for level in sorted(level_stats.keys()):
        stats = level_stats[level]
        pct = 100 * stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        color = Colors.OKGREEN if pct >= 50 else Colors.WARNING
        print(f"  Level {level}: {color}{stats['correct']}/{stats['total']} ({pct:.2f}%){Colors.ENDC}")

    wrong_answers = [(tid, r) for tid, r in results.items() if not r["correct"]]
    if wrong_answers:
        print(f"\n{Colors.FAIL}=== Wrong Answers ({len(wrong_answers)}) ==={Colors.ENDC}")
        for task_id, result in sorted(wrong_answers):
            print(f"\n  Task: {task_id}")
            print(f"  Level: {result['level']}")
            pred_display = result['predicted'][:100] + "..." if len(result['predicted']) > 100 else result['predicted']
            gt_display = result['ground_truth'][:100] + "..." if len(result['ground_truth']) > 100 else result['ground_truth']
            print(f"  Predicted: {pred_display}")
            print(f"  Ground Truth: {gt_display}")


def run_gaia_evaluation(config: dict) -> int:
    benchmark_path = select_gaia_benchmark_folder(config)
    if benchmark_path is None:
        print_info("Exiting.")
        return 0

    timestamp_path = select_gaia_timestamp(benchmark_path)
    if timestamp_path is None:
        print_info("Exiting.")
        return 0

    scenarios = select_gaia_scenario()
    if scenarios is None:
        print_info("Exiting.")
        return 0

    benchmark_name = benchmark_path.name
    print_info(f"Loading metadata for {benchmark_name}...")
    metadata = load_gaia_metadata(benchmark_name, config)
    print_success(f"Loaded {len(metadata)} task entries from metadata.")

    benchmark_type = benchmark_name.replace("GAIA-", "")

    for scenario in scenarios:
        print_info(f"Evaluating scenario: {scenario}...")
        answers, missing_tasks, results = evaluate_gaia_scenario(
            timestamp_path, scenario, metadata
        )

        if answers:
            jsonl_path = save_gaia_answers_jsonl(timestamp_path, scenario, answers)
        else:
            jsonl_path = Path("(not saved - no answers)")

        if results:
            summary = calculate_gaia_summary(
                timestamp_path, scenario, results, benchmark_type
            )
            summary_path = save_gaia_summary(timestamp_path, scenario, summary)
            print_success(f"Summary saved: {summary_path}")

        print_gaia_results(scenario, results, missing_tasks, jsonl_path)

    print_header("GAIA Evaluation Complete")
    return 0


def select_gpqa_benchmark_folder(config: dict) -> Optional[Path]:
    base_path = Path(config['base_path'])
    gpqa_folders = sorted([
        f for f in base_path.iterdir()
        if f.is_dir() and f.name.startswith("GPQA")
    ])

    if not gpqa_folders:
        print_error("No GPQA benchmark folders found in results/")
        return None

    print_header("Select GPQA Benchmark Folder")
    for i, folder in enumerate(gpqa_folders, 1):
        print(f"  [{i}] {folder.name}")

    while True:
        try:
            choice = input(f"\n{Colors.OKBLUE}Select folder (1-{len(gpqa_folders)}, or 'q' to quit): {Colors.ENDC}").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(gpqa_folders):
                selected = gpqa_folders[idx]
                print_success(f"Selected: {selected.name}")
                return selected
            print_error("Invalid selection. Try again.")
        except ValueError:
            print_error("Please enter a valid number.")


def select_gpqa_timestamp(benchmark_path: Path) -> Optional[Path]:
    timestamp_folders = sorted([
        f for f in benchmark_path.iterdir()
        if f.is_dir() and f.name[0].isdigit()
    ])

    if not timestamp_folders:
        print_error(f"No timestamp folders found in {benchmark_path.name}/")
        return None

    print_header("Select Timestamp")
    for i, folder in enumerate(timestamp_folders, 1):
        task_count = len([f for f in folder.iterdir() if f.is_dir()])
        print(f"  [{i}] {folder.name} ({task_count} tasks)")

    while True:
        try:
            choice = input(f"\n{Colors.OKBLUE}Select timestamp (1-{len(timestamp_folders)}, or 'q' to quit): {Colors.ENDC}").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(timestamp_folders):
                selected = timestamp_folders[idx]
                print_success(f"Selected: {selected.name}")
                return selected
            print_error("Invalid selection. Try again.")
        except ValueError:
            print_error("Please enter a valid number.")


def select_gpqa_scenario() -> Optional[List[str]]:
    print_header("Select Scenario")
    print("  [0] all (evaluate all scenarios)")
    for i, scenario in enumerate(AVAILABLE_SCENARIOS, 1):
        print(f"  [{i}] {scenario}")

    while True:
        try:
            choice = input(f"\n{Colors.OKBLUE}Select scenario (0-{len(AVAILABLE_SCENARIOS)}, or 'q' to quit): {Colors.ENDC}").strip()
            if choice.lower() == 'q':
                return None
            idx = int(choice)
            if idx == 0:
                return AVAILABLE_SCENARIOS
            elif 1 <= idx <= len(AVAILABLE_SCENARIOS):
                return [AVAILABLE_SCENARIOS[idx - 1]]
            print_error("Invalid selection. Try again.")
        except ValueError:
            print_error("Please enter a valid number.")


def load_gpqa_metadata(config: dict) -> Dict[str, dict]:
    metadata_path = Path(config['benchmark_path']) / "metadata.jsonl"

    if not metadata_path.exists():
        print_warning(f"Metadata file not found: {metadata_path}")
        return {}

    metadata = {}
    with open(metadata_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                entry = json.loads(line)
                task_id = entry.get("task_id")
                if task_id:
                    metadata[task_id] = entry

    return metadata


def parse_gpqa_final_answer(scenario_path: Path) -> Optional[str]:
    final_answer_path = scenario_path / "final_answer.txt"
    if final_answer_path.exists():
        try:
            with open(final_answer_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            match = re.search(r'(?i)final\s*answer\s*:\s*([A-Da-d])', content)
            if match:
                return match.group(1).upper()

            if content.upper() in ['A', 'B', 'C', 'D']:
                return content.upper()

        except Exception as e:
            print_warning(f"Error reading {final_answer_path}: {e}")

    merged_path = scenario_path / "merged_analysis.txt"
    if merged_path.exists():
        try:
            with open(merged_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            match = re.search(r'(?i)final\s*answer\s*:\s*([A-Da-d])', content)
            if match:
                return match.group(1).upper()

        except Exception as e:
            print_warning(f"Error reading {merged_path}: {e}")

    return None


def compare_gpqa_answers(predicted: str, ground_truth: str) -> bool:
    if predicted is None:
        return False

    pred_normalized = predicted.strip().upper()
    gt_normalized = ground_truth.strip().upper()

    return pred_normalized == gt_normalized


def load_gpqa_task_metrics(scenario_path: Path) -> dict:
    metrics_path = scenario_path / "metrics.json"
    default_metrics = {
        "duration_seconds": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "model": "unknown",
        "status": "unknown"
    }

    if not metrics_path.exists():
        return default_metrics

    try:
        with open(metrics_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        duration = data.get("task_duration", 0)

        input_tokens = 0
        output_tokens = 0
        model_name = "unknown"

        by_model = data.get("by_model", {})
        if by_model:
            model_name = list(by_model.keys())[0]
            model_data = by_model[model_name]
            input_tokens = model_data.get("prompt_tokens", 0)
            output_tokens = model_data.get("completion_tokens", 0)

        final_answer_path = scenario_path / "final_answer.txt"
        merged_path = scenario_path / "merged_analysis.txt"
        status = "success" if (final_answer_path.exists() or merged_path.exists()) else "failed"

        return {
            "duration_seconds": duration,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "model": model_name,
            "status": status
        }
    except Exception as e:
        print_warning(f"Error reading metrics from {metrics_path}: {e}")
        return default_metrics


def evaluate_gpqa_scenario(
    timestamp_path: Path,
    scenario: str,
    metadata: Dict[str, dict]
) -> Tuple[List[dict], List[str], Dict[str, dict]]:
    answers = []
    missing_tasks = []
    results = {}

    task_folders = [f for f in timestamp_path.iterdir() if f.is_dir() and f.name.startswith('gpqa_')]

    for task_folder in sorted(task_folders):
        task_id = task_folder.name
        scenario_path = task_folder / scenario

        if not scenario_path.exists():
            continue

        predicted_answer = parse_gpqa_final_answer(scenario_path)

        task_meta = metadata.get(task_id, {})
        question = task_meta.get("Question", "")
        level = task_meta.get("Level", 0)
        ground_truth = task_meta.get("Final answer", "")

        metrics = load_gpqa_task_metrics(scenario_path)

        if predicted_answer is None:
            missing_tasks.append(task_id)
            predicted_answer = ""
            is_correct = False
            status = "failed"
        else:
            is_correct = compare_gpqa_answers(predicted_answer, ground_truth) if ground_truth else False
            status = metrics["status"]

        answer_entry = {
            "task_id": task_id,
            "Question": question[:100] + "..." if len(question) > 100 else question,
            "Level": level,
            "Predicted": predicted_answer,
            "Ground_truth": ground_truth
        }
        answers.append(answer_entry)

        results[task_id] = {
            "predicted": predicted_answer,
            "ground_truth": ground_truth,
            "level": level,
            "correct": is_correct,
            "status": status,
            "duration_seconds": metrics["duration_seconds"],
            "input_tokens": metrics["input_tokens"],
            "output_tokens": metrics["output_tokens"],
            "model": metrics["model"]
        }

    return answers, missing_tasks, results


def save_gpqa_answers_jsonl(timestamp_path: Path, scenario: str, answers: List[dict]) -> Path:
    output_path = timestamp_path / f"{scenario}_answers.jsonl"

    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in answers:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    return output_path


def calculate_gpqa_summary(
    timestamp_path: Path,
    scenario: str,
    results: Dict[str, dict],
    benchmark_name: str
) -> dict:
    if not results:
        return {}

    timestamp = timestamp_path.name

    model = "unknown"
    for r in results.values():
        if r.get("model") and r.get("model") != "unknown":
            model = r["model"]
            break

    total = len(results)
    correct = sum(1 for r in results.values() if r["correct"])
    accuracy = (correct / total * 100) if total > 0 else 0

    total_input_tokens = sum(r.get("input_tokens", 0) for r in results.values())
    total_output_tokens = sum(r.get("output_tokens", 0) for r in results.values())
    total_duration = sum(r.get("duration_seconds", 0) for r in results.values())

    level_stats = {}
    for task_id, result in results.items():
        level = result.get("level", 0)
        if level not in level_stats:
            level_stats[level] = {
                "total": 0,
                "correct": 0,
                "total_tokens": 0,
                "total_time": 0
            }
        level_stats[level]["total"] += 1
        level_stats[level]["total_tokens"] += result.get("input_tokens", 0) + result.get("output_tokens", 0)
        level_stats[level]["total_time"] += result.get("duration_seconds", 0)
        if result["correct"]:
            level_stats[level]["correct"] += 1

    for level in level_stats:
        stats = level_stats[level]
        stats["accuracy"] = round(stats["correct"] / stats["total"] * 100, 2) if stats["total"] > 0 else 0
        stats["avg_tokens"] = round(stats["total_tokens"] / stats["total"]) if stats["total"] > 0 else 0
        stats["avg_time"] = round(stats["total_time"] / stats["total"], 2) if stats["total"] > 0 else 0
        del stats["total_tokens"]
        del stats["total_time"]

    results_array = []
    for task_id, result in sorted(results.items()):
        results_array.append({
            "task_id": task_id,
            "level": result.get("level", 0),
            "correct": result["correct"],
            "status": result.get("status", "unknown"),
            "predicted": result["predicted"],
            "ground_truth": result["ground_truth"],
            "tokens": result.get("input_tokens", 0) + result.get("output_tokens", 0),
            "duration_seconds": result.get("duration_seconds", 0)
        })

    summary = {
        "timestamp": timestamp,
        "model": model,
        "benchmark": benchmark_name,
        "scenario": scenario,
        "total_duration_seconds": round(total_duration, 2),
        "statistics": {
            "total": total,
            "correct": correct,
            "accuracy": round(accuracy, 2),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens,
            "avg_tokens": round((total_input_tokens + total_output_tokens) / total) if total > 0 else 0,
            "avg_time": round(total_duration / total, 2) if total > 0 else 0
        },
        "level_statistics": level_stats,
        "results": results_array
    }

    return summary


def save_gpqa_summary(timestamp_path: Path, scenario: str, summary: dict) -> Path:
    output_path = timestamp_path / f"{scenario}_summary.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return output_path


def print_gpqa_results(
    scenario: str,
    results: Dict[str, dict],
    missing_tasks: List[str],
    jsonl_path: Path
):
    print(f"\n{'='*60}")
    print(f"Scenario: {scenario}")
    print(f"{'='*60}")

    if missing_tasks:
        print(f"\n{Colors.WARNING}=== Failed Tasks (no valid answer) ==={Colors.ENDC}")
        for task_id in sorted(missing_tasks):
            print(f"  - {task_id}")
        print(f"Total missing: {len(missing_tasks)}")

    if not results:
        print_warning("No results to evaluate.")
        return

    total_correct = sum(1 for r in results.values() if r["correct"])
    total_count = len(results)

    level_stats = {}
    for task_id, result in results.items():
        level = result["level"]
        if level not in level_stats:
            level_stats[level] = {"correct": 0, "total": 0}
        level_stats[level]["total"] += 1
        if result["correct"]:
            level_stats[level]["correct"] += 1

    print(f"\n{Colors.BOLD}=== Evaluation Results ==={Colors.ENDC}")
    print_info(f"JSONL saved: {jsonl_path}")
    print(f"\n{Colors.BOLD}Overall: {total_correct}/{total_count} ({100*total_correct/total_count:.2f}%){Colors.ENDC}")

    for level in sorted(level_stats.keys()):
        stats = level_stats[level]
        pct = 100 * stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        color = Colors.OKGREEN if pct >= 50 else Colors.WARNING
        print(f"  Level {level}: {color}{stats['correct']}/{stats['total']} ({pct:.2f}%){Colors.ENDC}")

    wrong_answers = [(tid, r) for tid, r in results.items() if not r["correct"]]
    if wrong_answers:
        print(f"\n{Colors.FAIL}=== Wrong Answers ({len(wrong_answers)}) ==={Colors.ENDC}")
        for task_id, result in sorted(wrong_answers)[:20]:
            print(f"\n  Task: {task_id}")
            print(f"  Level: {result['level']}")
            print(f"  Predicted: {result['predicted'] or '(empty)'}")
            print(f"  Ground Truth: {result['ground_truth']}")
        if len(wrong_answers) > 20:
            print(f"\n  ... and {len(wrong_answers) - 20} more wrong answers")


def run_gpqa_evaluation(config: dict) -> int:
    benchmark_path = select_gpqa_benchmark_folder(config)
    if benchmark_path is None:
        print_info("Exiting.")
        return 0

    timestamp_path = select_gpqa_timestamp(benchmark_path)
    if timestamp_path is None:
        print_info("Exiting.")
        return 0

    scenarios = select_gpqa_scenario()
    if scenarios is None:
        print_info("Exiting.")
        return 0

    print_info(f"Loading metadata for GPQA-Diamond...")
    metadata = load_gpqa_metadata(config)
    print_success(f"Loaded {len(metadata)} task entries from metadata.")

    for scenario in scenarios:
        print_info(f"Evaluating scenario: {scenario}...")
        answers, missing_tasks, results = evaluate_gpqa_scenario(
            timestamp_path, scenario, metadata
        )

        if answers:
            jsonl_path = save_gpqa_answers_jsonl(timestamp_path, scenario, answers)
        else:
            jsonl_path = Path("(not saved - no answers)")

        if results:
            summary = calculate_gpqa_summary(
                timestamp_path, scenario, results, "GPQA_Diamond"
            )
            summary_path = save_gpqa_summary(timestamp_path, scenario, summary)
            print_success(f"Summary saved: {summary_path}")

        print_gpqa_results(scenario, results, missing_tasks, jsonl_path)

    print_header("GPQA-Diamond Evaluation Complete")
    return 0


def is_timestamp_folder(folder_name: str) -> bool:
    import re
    return bool(re.match(r'^\d{8}_\d{6}', folder_name))


def select_timestamp_folder(parent_folder: Path) -> Optional[Path]:
    timestamp_folders = []
    subfolder_candidates = []
    for item in sorted(parent_folder.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            task_count = len([d for d in item.iterdir() if d.is_dir() and not d.name.startswith('.')])
            if is_timestamp_folder(item.name):
                timestamp_folders.append((item, task_count))
            else:
                has_tasks = False
                for subitem in item.iterdir():
                    if subitem.is_dir() and not subitem.name.startswith('.'):
                        scenario_check = [s for s in AVAILABLE_SCENARIOS if (subitem / s).exists()]
                        if scenario_check:
                            has_tasks = True
                            break
                if has_tasks:
                    subfolder_candidates.append((item, task_count))

    all_folders = timestamp_folders + subfolder_candidates

    if not all_folders:
        return None

    print_header("Select Sub Folder")
    print_info(f"Found {len(all_folders)} folders in {parent_folder.name}\n")

    print(f"{Colors.BOLD}Available folders:{Colors.ENDC}")
    for idx, (folder, task_count) in enumerate(all_folders, 1):
        print(f"  [{idx:2d}] {folder.name} ({task_count} tasks)")

    while True:
        choice = input(f"\n{Colors.OKBLUE}Select folder number (1-{len(all_folders)}): {Colors.ENDC}").strip()

        if not choice.isdigit():
            print_error("Please enter a valid number")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(all_folders):
            print_error(f"Please enter a number between 1 and {len(all_folders)}")
            continue

        selected_folder = all_folders[idx][0]
        print_success(f"Selected: {selected_folder.name}")
        return selected_folder


def select_target_folder(config: dict) -> Path:
    print_header(f"Select Target Folder - {config['name']}")

    base_path = Path(config['base_path'])

    if not base_path.exists():
        print_error(f"Base folder does not exist: {base_path}")
        print_info("Please enter the folder path manually.")
        folder_path = input(f"{Colors.OKBLUE}Enter folder path: {Colors.ENDC}").strip()

        if not folder_path.startswith('/'):
            folder_path = os.path.join('input_your_path', folder_path)

        return Path(folder_path)

    folder_prefix = config.get('folder_prefix', '')

    subdirs = []
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            if folder_prefix and not item.name.startswith(folder_prefix):
                continue
            has_valid_structure = False
            for subitem in item.iterdir():
                if subitem.is_dir() and not subitem.name.startswith('.'):
                    scenario_check = [s for s in AVAILABLE_SCENARIOS if (subitem / s).exists()]
                    if scenario_check:
                        has_valid_structure = True
                        break
                    for taskitem in subitem.iterdir():
                        if taskitem.is_dir() and not taskitem.name.startswith('.'):
                            task_scenario_check = [s for s in AVAILABLE_SCENARIOS if (taskitem / s).exists()]
                            if task_scenario_check:
                                has_valid_structure = True
                                break
                    if has_valid_structure:
                        break
            if has_valid_structure:
                subdirs.append(item)

    if not subdirs:
        print_error(f"No valid result folders found matching '{folder_prefix}*'")
        return None

    subdirs = sorted(subdirs, key=lambda x: x.name, reverse=True)

    print(f"\n{Colors.BOLD}Available result folders:{Colors.ENDC}")
    for idx, folder in enumerate(subdirs, 1):
        task_count = len([d for d in folder.iterdir() if d.is_dir() and not d.name.startswith('.')])
        print(f"  [{idx:2d}] {folder.name} ({task_count} tasks)")

    while True:
        choice = input(f"\n{Colors.OKBLUE}Select folder number (1-{len(subdirs)}): {Colors.ENDC}").strip()

        if not choice.isdigit():
            print_error("Please enter a valid number")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(subdirs):
            print_error(f"Please enter a number between 1 and {len(subdirs)}")
            continue

        selected_folder = subdirs[idx]
        print_success(f"Selected: {selected_folder.name}")

        timestamp_folder = select_timestamp_folder(selected_folder)
        if timestamp_folder:
            return timestamp_folder

        return selected_folder


def scan_scenarios(base_path: Path) -> Dict[str, List[Tuple[str, bool]]]:
    print_info("Scanning scenarios...")

    task_scenarios = {}

    for task_dir in sorted(base_path.iterdir()):
        if not task_dir.is_dir() or task_dir.name.startswith('.'):
            continue

        task_name = task_dir.name
        scenarios = []

        for scenario in AVAILABLE_SCENARIOS:
            scenario_path = task_dir / scenario
            if scenario_path.exists() and scenario_path.is_dir():
                app_py = scenario_path / "app.py"
                if app_py.exists():
                    scenarios.append((scenario, True))
                else:
                    scenarios.append((scenario, False))
                    print_warning(f"{task_name}/{scenario}: app.py not found (will count as 0%)")

        if scenarios:
            task_scenarios[task_name] = scenarios

    return task_scenarios


def select_scenarios_interactive(task_scenarios: Dict[str, List[Tuple[str, bool]]]) -> List[Tuple[str, str, bool]]:
    print_header("Select Scenarios")

    total_tasks = len(task_scenarios)
    total_scenarios = sum(len(scenarios) for scenarios in task_scenarios.values())

    print_info(f"Found tasks: {total_tasks}")
    print_info(f"Total scenarios: {total_scenarios}\n")

    print("Selection options:")
    print("  [1] Vanilla only")
    print("  [2] All chaos scenarios only (exclude vanilla)")
    print("  [3] Select specific scenarios")
    print("  [4] Test all scenarios")
    print("  [5] Select specific tasks only\n")

    while True:
        choice = input(f"{Colors.OKBLUE}Select (1-5): {Colors.ENDC}").strip()

        if choice == '1':
            selected = []
            for task, scenarios in task_scenarios.items():
                for scenario_name, has_app_py in scenarios:
                    if scenario_name == 'vanilla':
                        selected.append((task, scenario_name, has_app_py))
            break

        elif choice == '2':
            selected = []
            for task, scenarios in task_scenarios.items():
                for scenario_name, has_app_py in scenarios:
                    if scenario_name != 'vanilla':
                        selected.append((task, scenario_name, has_app_py))
            break

        elif choice == '3':
            print("\nAvailable scenarios:")
            for i, scenario in enumerate(AVAILABLE_SCENARIOS, 1):
                print(f"  [{i}] {scenario}")

            scenario_input = input(f"\n{Colors.OKBLUE}Select scenarios (comma-separated, e.g., 1,2,3): {Colors.ENDC}").strip()
            selected_indices = [int(x.strip()) - 1 for x in scenario_input.split(',')]
            selected_scenario_names = [AVAILABLE_SCENARIOS[i] for i in selected_indices
                                      if 0 <= i < len(AVAILABLE_SCENARIOS)]

            selected = []
            for task, scenarios in task_scenarios.items():
                for scenario_name, has_app_py in scenarios:
                    if scenario_name in selected_scenario_names:
                        selected.append((task, scenario_name, has_app_py))
            break

        elif choice == '4':
            selected = [(task, scenario_name, has_app_py)
                       for task, scenarios in task_scenarios.items()
                       for scenario_name, has_app_py in scenarios]
            break

        elif choice == '5':
            print("\nAvailable tasks:")
            task_list = sorted(task_scenarios.keys())
            for i, task in enumerate(task_list, 1):
                print(f"  [{i:2d}] {task} ({len(task_scenarios[task])} scenarios)")

            task_input = input(f"\n{Colors.OKBLUE}Select tasks (comma-separated, e.g., 1,2,3): {Colors.ENDC}").strip()
            selected_indices = [int(x.strip()) - 1 for x in task_input.split(',')]
            selected_tasks = [task_list[i] for i in selected_indices if 0 <= i < len(task_list)]

            selected = [(task, scenario_name, has_app_py)
                       for task in selected_tasks
                       for scenario_name, has_app_py in task_scenarios[task]]
            break

        else:
            print_error("Invalid selection. Please select 1-5.")

    print_success(f"{len(selected)} scenarios selected\n")
    return selected


def kill_processes_on_port(port: int):
    try:
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        pids = result.stdout.strip().split('\n')
        for pid in pids:
            if pid:
                try:
                    os.kill(int(pid), signal.SIGKILL)
                    print_info(f"Killed process {pid} on port {port}")
                except ProcessLookupError:
                    pass
        time.sleep(1)
    except Exception as e:
        print_warning(f"Error cleaning port: {e}")


def inject_test_data(task: str, scenario_path: Path, config: dict) -> bool:
    source_data = Path(config['test_data_base']) / task
    dest_data = scenario_path / "data"

    if not source_data.exists():
        print_error(f"Test data not found: {source_data}")
        return False

    try:
        if dest_data.exists():
            backup_path = scenario_path / "data_backup"
            if backup_path.exists():
                shutil.rmtree(backup_path)
            shutil.move(str(dest_data), str(backup_path))
            print_info(f"Backed up existing data: data -> data_backup")

        shutil.copytree(str(source_data), str(dest_data))
        print_success(f"Data injection completed: {task}")
        return True

    except Exception as e:
        print_error(f"Data injection failed: {e}")
        return False


def cleanup_test_data(scenario_path: Path):
    dest_data = scenario_path / "data"
    backup_path = scenario_path / "data_backup"

    try:
        if dest_data.exists():
            shutil.rmtree(dest_data)

        if backup_path.exists():
            shutil.move(str(backup_path), str(dest_data))
            print_info(f"Restored original data from backup")
    except Exception as e:
        print_warning(f"Data cleanup failed: {e}")


def run_test_for_scenario(task: str, scenario_path: Path, config: dict) -> Dict:
    global _skip_requested

    if config['name'] == 'GUI Applications':
        reset_skip_flag()

    test_script_name = config['test_script_pattern'].format(task=task)
    test_script = Path(config['testcode_dir']) / test_script_name

    if not test_script.exists():
        return {
            'status': 'error',
            'message': f'Test script not found: {test_script}',
            'total_tests': 0,
            'total_basic': 0,
            'total_advanced': 0,
            'basic_passed': 0,
            'advanced_passed': 0,
            'total_passed': 0,
            'basic_success_rate': 0,
            'advanced_success_rate': 0
        }

    if config['requires_server']:
        kill_processes_on_port(config['server_port'])

    test_exec_dir = scenario_path / "test_exec"
    test_exec_dir.mkdir(exist_ok=True)

    try:
        env = os.environ.copy()
        if config['test_data_base'] is not None:
            test_modules_dir = str(Path(config['test_data_base']).parent)
        else:
            test_modules_dir = str(Path(config['testcode_dir']).parent)
        env['PYTHONPATH'] = f"{scenario_path}:{config['testcode_dir']}:{test_modules_dir}"
        env['PYTHONUNBUFFERED'] = '1'

        app_py_path = scenario_path / config['entry_file']

        if config['name'] == 'GUI Applications':
            print_info(f"Starting test execution ({config['framework']})... (Press 's' to skip)")
        else:
            print_info(f"Starting test execution ({config['framework']})...")

        cmd = [sys.executable, '-u', str(test_script), str(app_py_path)]

        if config['name'] == 'GUI Applications':
            cmd = ['xvfb-run', '-a', '--server-args=-screen 0 1024x768x24'] + cmd

        process = subprocess.Popen(
            cmd,
            cwd=str(test_exec_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
            errors='replace'
        )

        output_lines = []
        start_time = time.time()

        while True:
            if time.time() - start_time > config['test_timeout']:
                process.kill()
                process.wait()
                raise subprocess.TimeoutExpired(process.args, config['test_timeout'])

            if config['name'] == 'GUI Applications':
                if _skip_requested:
                    process.kill()
                    process.wait()
                    print_skip(f"Test skipped by user (pressed 's')")

                    partial_basic = 0
                    partial_advanced = 0
                    script_total_basic = 0
                    script_total_advanced = 0

                    for line in output_lines:
                        if '... ok' in line.lower() or '...ok' in line.lower():
                            if 'test_basic' in line.lower():
                                partial_basic += 1
                            elif 'test_advanced' in line.lower() or 'test_logic' in line.lower():
                                partial_advanced += 1

                    try:
                        with open(test_script, 'r') as f:
                            script_content = f.read()
                        total_basic_match = re.search(r'total_basic\s*=\s*(\d+)', script_content)
                        total_advanced_match = re.search(r'total_advanced\s*=\s*(\d+)', script_content)
                        if total_basic_match:
                            script_total_basic = int(total_basic_match.group(1))
                        if total_advanced_match:
                            script_total_advanced = int(total_advanced_match.group(1))
                    except:
                        pass

                    partial_total = partial_basic + partial_advanced
                    partial_basic_rate = (partial_basic / script_total_basic * 100) if script_total_basic > 0 else 0
                    partial_advanced_rate = (partial_advanced / script_total_advanced * 100) if script_total_advanced > 0 else 0

                    return {
                        'status': 'skipped',
                        'message': 'Skipped by user (partial results included)',
                        'total_tests': script_total_basic + script_total_advanced,
                        'total_basic': script_total_basic,
                        'total_advanced': script_total_advanced,
                        'basic_passed': partial_basic,
                        'advanced_passed': partial_advanced,
                        'total_passed': partial_total,
                        'basic_success_rate': round(partial_basic_rate, 3),
                        'advanced_success_rate': round(partial_advanced_rate, 3)
                    }

                ready_read, _, _ = select.select([process.stdout], [], [], 0.1)

                if ready_read:
                    line = process.stdout.readline()
                else:
                    line = None
            else:
                line = process.stdout.readline()

            if line:
                line_stripped = line.rstrip()

                if 'FAIL' in line or 'ERROR' in line or 'Exception' in line:
                    print(f"  {Colors.FAIL}{line_stripped}{Colors.ENDC}")
                elif 'OK' in line or 'PASS' in line or 'SUCCESS' in line:
                    print(f"  {Colors.OKGREEN}{line_stripped}{Colors.ENDC}")
                elif 'test_' in line:
                    print(f"  {Colors.OKBLUE}{line_stripped}{Colors.ENDC}")
                else:
                    print(f"  {Colors.OKCYAN}{line_stripped}{Colors.ENDC}")

                output_lines.append(line)

            if process.poll() is not None:
                for remaining_line in process.stdout:
                    line_stripped = remaining_line.rstrip()
                    if 'FAIL' in remaining_line or 'ERROR' in remaining_line or 'Exception' in remaining_line:
                        print(f"  {Colors.FAIL}{line_stripped}{Colors.ENDC}")
                    elif 'OK' in remaining_line or 'PASS' in remaining_line or 'SUCCESS' in remaining_line:
                        print(f"  {Colors.OKGREEN}{line_stripped}{Colors.ENDC}")
                    elif 'test_' in remaining_line:
                        print(f"  {Colors.OKBLUE}{line_stripped}{Colors.ENDC}")
                    else:
                        print(f"  {Colors.OKCYAN}{line_stripped}{Colors.ENDC}")
                    output_lines.append(remaining_line)
                break

        output = ''.join(output_lines)
        result_returncode = process.returncode

        if "ERROR: Could not find app.py" in output or "Could not find app.py" in output:
            return {
                'status': 'error',
                'message': 'Test script could not find app.py',
                'total_tests': 0,
                'total_basic': 0,
                'total_advanced': 0,
                'basic_passed': 0,
                'advanced_passed': 0,
                'total_passed': 0,
                'basic_success_rate': 0,
                'advanced_success_rate': 0
            }

        total_tests = 0
        basic_passed = 0
        advanced_passed = 0
        total_basic = 0
        total_advanced = 0

        basic_match = re.search(r"'basic':\s*(\d+)", output)
        advanced_match = re.search(r"'advanced':\s*(\d+)", output)
        total_match = re.search(r"'total':\s*(\d+)", output)
        total_basic_match = re.search(r"'total_basic':\s*(\d+)", output)
        total_advanced_match = re.search(r"'total_advanced':\s*(\d+)", output)

        if basic_match and advanced_match and total_match:
            basic_passed = int(basic_match.group(1))
            advanced_passed = int(advanced_match.group(1))
            total_tests = int(total_match.group(1))
            if total_basic_match:
                total_basic = int(total_basic_match.group(1))
            if total_advanced_match:
                total_advanced = int(total_advanced_match.group(1))
        else:
            success_match = re.search(r'SUCCESS:\s*(\d+)', output)
            failures_match = re.search(r'FAILURES:\s*(\d+)', output)
            errors_match = re.search(r'ERRORS:\s*(\d+)', output)

            if success_match:
                success_count = int(success_match.group(1))
                failures_count = int(failures_match.group(1)) if failures_match else 0
                errors_count = int(errors_match.group(1)) if errors_match else 0

                total_tests = success_count + failures_count + errors_count

                total_basic = (total_tests + 1) // 2
                total_advanced = total_tests - total_basic
                basic_passed = success_count // 2
                advanced_passed = success_count - basic_passed

        passed = basic_passed + advanced_passed

        if result_returncode != 0 and total_tests == 0:
            return {
                'status': 'error',
                'message': f'Test script execution failed (exit code: {result_returncode})',
                'total_tests': 0,
                'total_basic': 0,
                'total_advanced': 0,
                'basic_passed': 0,
                'advanced_passed': 0,
                'total_passed': 0,
                'basic_success_rate': 0,
                'advanced_success_rate': 0
            }

        status = 'passed' if passed == total_tests and total_tests > 0 else 'failed'

        basic_success_rate = (basic_passed / total_basic * 100) if total_basic > 0 else 0
        advanced_success_rate = (advanced_passed / total_advanced * 100) if total_advanced > 0 else 0

        return {
            'status': status,
            'total_tests': total_tests,
            'total_basic': total_basic,
            'total_advanced': total_advanced,
            'basic_passed': basic_passed,
            'advanced_passed': advanced_passed,
            'total_passed': passed,
            'basic_success_rate': round(basic_success_rate, 3),
            'advanced_success_rate': round(advanced_success_rate, 3)
        }

    except subprocess.TimeoutExpired:
        return {
            'status': 'timeout',
            'message': f'Test timeout ({config["test_timeout"]}s)',
            'total_tests': 0,
            'total_basic': 0,
            'total_advanced': 0,
            'basic_passed': 0,
            'advanced_passed': 0,
            'total_passed': 0,
            'basic_success_rate': 0,
            'advanced_success_rate': 0
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'total_tests': 0,
            'total_basic': 0,
            'total_advanced': 0,
            'basic_passed': 0,
            'advanced_passed': 0,
            'total_passed': 0,
            'basic_success_rate': 0,
            'advanced_success_rate': 0
        }

    finally:
        if config['requires_server']:
            kill_processes_on_port(config['server_port'])

        try:
            if test_exec_dir.exists():
                shutil.rmtree(test_exec_dir)
        except Exception as e:
            print_warning(f"Failed to clean test execution directory: {e}")


def generate_results_report(target_folder: Path, all_results: List[Dict],
                           scenarios_tested: List[str]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    total_scenarios = len(all_results)
    fully_passed = sum(1 for r in all_results if r.get('status') == 'passed')
    partially_passed = sum(1 for r in all_results
                          if r.get('status') == 'failed' and r.get('total_passed', 0) > 0)
    failed = sum(1 for r in all_results if r.get('status') in ['failed', 'error', 'timeout'])
    skipped = sum(1 for r in all_results if r.get('status') == 'skipped')
    no_app = sum(1 for r in all_results if r.get('status') == 'no_app')

    total_tests = sum(r.get('total_tests', 0) for r in all_results)
    total_passed = sum(r.get('total_passed', 0) for r in all_results)

    total_basic = sum(r.get('total_basic', 0) for r in all_results)
    total_advanced = sum(r.get('total_advanced', 0) for r in all_results)
    basic_passed = sum(r.get('basic_passed', 0) for r in all_results)
    advanced_passed = sum(r.get('advanced_passed', 0) for r in all_results)

    basic_rates = []
    advanced_rates = []
    for r in all_results:
        if r.get('status') in ['skipped', 'no_app']:
            basic_rates.append(0)
            advanced_rates.append(0)
        else:
            basic_rates.append(r.get('basic_success_rate', 0))
            advanced_rates.append(r.get('advanced_success_rate', 0))
    avg_basic_rate = sum(basic_rates) / len(basic_rates) if basic_rates else 0
    avg_advanced_rate = sum(advanced_rates) / len(advanced_rates) if advanced_rates else 0

    scenario_stats = {}
    for scenario in set(scenarios_tested):
        scenario_results = [r for r in all_results if r.get('scenario') == scenario]
        if scenario_results:
            scenario_total_basic = sum(r.get('total_basic', 0) for r in scenario_results)
            scenario_total_advanced = sum(r.get('total_advanced', 0) for r in scenario_results)
            scenario_basic_passed = sum(r.get('basic_passed', 0) for r in scenario_results)
            scenario_advanced_passed = sum(r.get('advanced_passed', 0) for r in scenario_results)

            scenario_basic_rates = []
            scenario_advanced_rates = []
            for r in scenario_results:
                if r.get('status') in ['skipped', 'no_app']:
                    scenario_basic_rates.append(0)
                    scenario_advanced_rates.append(0)
                else:
                    scenario_basic_rates.append(r.get('basic_success_rate', 0))
                    scenario_advanced_rates.append(r.get('advanced_success_rate', 0))
            scenario_avg_basic_rate = sum(scenario_basic_rates) / len(scenario_basic_rates) if scenario_basic_rates else 0
            scenario_avg_advanced_rate = sum(scenario_advanced_rates) / len(scenario_advanced_rates) if scenario_advanced_rates else 0

            scenario_stats[scenario] = {
                'total': len(scenario_results),
                'passed': sum(1 for r in scenario_results if r.get('status') == 'passed'),
                'total_tests': sum(r.get('total_tests', 0) for r in scenario_results),
                'total_passed': sum(r.get('total_passed', 0) for r in scenario_results),
                'total_basic': scenario_total_basic,
                'total_advanced': scenario_total_advanced,
                'basic_passed': scenario_basic_passed,
                'advanced_passed': scenario_advanced_passed,
                'basic_success_rate': round(scenario_basic_passed / scenario_total_basic * 100, 3) if scenario_total_basic > 0 else 0,
                'advanced_success_rate': round(scenario_advanced_passed / scenario_total_advanced * 100, 3) if scenario_total_advanced > 0 else 0,
                'avg_basic_success_rate': round(scenario_avg_basic_rate, 3),
                'avg_advanced_success_rate': round(scenario_avg_advanced_rate, 3)
            }

    report = {
        'scenarios_tested': list(set(scenarios_tested)),
        'statistics': {
            'total_scenarios': total_scenarios,
            'fully_passed_scenarios': fully_passed,
            'partially_passed_scenarios': partially_passed,
            'failed_scenarios': failed,
            'skipped_scenarios': skipped,
            'no_app_scenarios': no_app,
            'total_tests': total_tests,
            'total_passed': total_passed,
            'pass_rate': f"{(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "0%",
            'total_basic': total_basic,
            'total_advanced': total_advanced,
            'basic_passed': basic_passed,
            'advanced_passed': advanced_passed,
            'basic_success_rate': round(basic_passed / total_basic * 100, 3) if total_basic > 0 else 0,
            'advanced_success_rate': round(advanced_passed / total_advanced * 100, 3) if total_advanced > 0 else 0,
            'avg_basic_success_rate': round(avg_basic_rate, 3),
            'avg_advanced_success_rate': round(avg_advanced_rate, 3)
        },
        'scenario_statistics': scenario_stats,
        'results': all_results
    }

    output_file = target_folder / f"test_results_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return str(output_file)


def run_software_evaluation(config: dict) -> int:
    target_folder = select_target_folder(config)

    if not target_folder:
        print_error("No folder selected")
        return 1

    task_scenarios = scan_scenarios(target_folder)

    if not task_scenarios:
        print_error("No testable scenarios found")
        return 1

    selected = select_scenarios_interactive(task_scenarios)

    if not selected:
        print_error("No scenarios selected")
        return 1

    print_header(f"Running Tests ({len(selected)} scenarios) - {config['name']}")

    if config['name'] == 'GUI Applications':
        print_info("Hint: Press 's' during test execution to skip current test\n")

    all_results = []
    start_time = time.time()

    if config['name'] == 'GUI Applications':
        setup_terminal()
        start_key_listener()

    try:
        for idx, (task, scenario, has_app_py) in enumerate(selected, 1):
            scenario_path = target_folder / task / scenario

            print(f"\n[{idx}/{len(selected)}] {task}/{scenario}")
            print("-" * 80)

            if not has_app_py:
                result = {
                    'task': task,
                    'scenario': scenario,
                    'status': 'no_app',
                    'message': 'app.py not found',
                    'total_tests': 0,
                    'total_basic': 0,
                    'total_advanced': 0,
                    'basic_passed': 0,
                    'advanced_passed': 0,
                    'total_passed': 0,
                    'basic_success_rate': 0,
                    'advanced_success_rate': 0,
                    'execution_time': 0
                }
                all_results.append(result)
                print_error(f"No app.py - counted as 0%")
                continue

            if config['requires_data_injection']:
                if not inject_test_data(task, scenario_path, config):
                    result = {
                        'task': task,
                        'scenario': scenario,
                        'status': 'error',
                        'message': 'Data injection failed',
                        'total_tests': 0,
                        'total_basic': 0,
                        'total_advanced': 0,
                        'basic_passed': 0,
                        'advanced_passed': 0,
                        'total_passed': 0,
                        'basic_success_rate': 0,
                        'advanced_success_rate': 0,
                        'execution_time': 0
                    }
                    all_results.append(result)
                    continue

            test_start = time.time()
            test_result = run_test_for_scenario(task, scenario_path, config)
            test_time = time.time() - test_start

            if config['requires_data_injection']:
                cleanup_test_data(scenario_path)

            result = {
                'task': task,
                'scenario': scenario,
                'execution_time': round(test_time, 2),
                **test_result
            }
            all_results.append(result)

            if result['status'] == 'passed':
                print_success(f"Passed: Basic {result.get('basic_passed', 0)}/{result.get('total_basic', 0)} "
                             f"({result.get('basic_success_rate', 0):.3f}%), "
                             f"Advanced {result.get('advanced_passed', 0)}/{result.get('total_advanced', 0)} "
                             f"({result.get('advanced_success_rate', 0):.3f}%) "
                             f"[{test_time:.1f}s]")
            elif result['status'] == 'failed':
                print_warning(f"Failed: Basic {result.get('basic_passed', 0)}/{result.get('total_basic', 0)} "
                             f"({result.get('basic_success_rate', 0):.3f}%), "
                             f"Advanced {result.get('advanced_passed', 0)}/{result.get('total_advanced', 0)} "
                             f"({result.get('advanced_success_rate', 0):.3f}%) "
                             f"[{test_time:.1f}s]")
            elif result['status'] == 'skipped':
                print_skip(f"Skipped by user [{test_time:.1f}s]")
            else:
                print_error(f"{result['status']}: {result.get('message', 'Unknown error')}")
    finally:
        if config['name'] == 'GUI Applications':
            stop_key_listener()
            restore_terminal()

    total_time = time.time() - start_time
    scenarios_tested = [scenario for _, scenario, _ in selected]
    output_file = generate_results_report(target_folder, all_results, scenarios_tested)

    print_header("Test Completed")
    print_info(f"Application Type: {config['name']}")
    print_info(f"Total execution time: {total_time:.1f}s")
    print_info(f"Results saved: {output_file}")

    total_tests = sum(r.get('total_tests', 0) for r in all_results)
    total_passed = sum(r.get('total_passed', 0) for r in all_results)
    fully_passed = sum(1 for r in all_results if r.get('status') == 'passed')

    total_basic = sum(r.get('total_basic', 0) for r in all_results)
    total_advanced = sum(r.get('total_advanced', 0) for r in all_results)
    basic_passed = sum(r.get('basic_passed', 0) for r in all_results)
    advanced_passed = sum(r.get('advanced_passed', 0) for r in all_results)

    basic_rates = []
    advanced_rates = []
    for r in all_results:
        if r.get('status') in ['skipped', 'no_app']:
            basic_rates.append(0)
            advanced_rates.append(0)
        else:
            basic_rates.append(r.get('basic_success_rate', 0))
            advanced_rates.append(r.get('advanced_success_rate', 0))

    avg_basic_rate = sum(basic_rates) / len(basic_rates) if basic_rates else 0
    avg_advanced_rate = sum(advanced_rates) / len(advanced_rates) if advanced_rates else 0

    failed_tasks = sum(1 for r in all_results if r.get('status') in ['failed', 'error', 'timeout'])
    skipped_tasks = sum(1 for r in all_results if r.get('status') == 'skipped')
    no_app_tasks = sum(1 for r in all_results if r.get('status') == 'no_app')
    setup_failed = sum(1 for r in all_results
                       if r.get('total_basic', 0) == 0 and r.get('total_advanced', 0) <= 1
                       and r.get('status') not in ['skipped', 'no_app'])

    print(f"\n{Colors.BOLD}Statistics:{Colors.ENDC}")
    print(f"  Basic SR Average: {Colors.OKGREEN}{avg_basic_rate:.3f}%{Colors.ENDC}")
    print(f"  Advanced SR Average: {Colors.OKGREEN}{avg_advanced_rate:.3f}%{Colors.ENDC}")
    print(f"  Total Tasks: {len(all_results)}")
    print(f"  Failed Tasks: {Colors.FAIL}{failed_tasks}{Colors.ENDC}")
    if skipped_tasks > 0:
        print(f"  Skipped Tasks: {Colors.WARNING}{skipped_tasks}{Colors.ENDC}")
    if no_app_tasks > 0:
        print(f"  No app.py: {Colors.WARNING}{no_app_tasks}{Colors.ENDC}")
    print(f"  Setup Failed: {Colors.WARNING}{setup_failed}{Colors.ENDC}")

    return 0


def main():
    print_header("CaMP Unified Evaluation Pipeline")

    global CURRENT_CONFIG
    CURRENT_CONFIG = select_app_type()

    if CURRENT_CONFIG['name'] == 'GAIA Benchmark':
        return run_gaia_evaluation(CURRENT_CONFIG)
    elif CURRENT_CONFIG['name'] == 'GPQA-Diamond Benchmark':
        return run_gpqa_evaluation(CURRENT_CONFIG)
    else:
        return run_software_evaluation(CURRENT_CONFIG)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print_error("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
