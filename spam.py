
import random
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "commit-log.md"
MAX_BURST = 20

MESSAGES = [
    "feat: added absolutely unnecessary innovation",
    "fix: fixed a problem nobody reported",
    "docs: documented my questionable decisions",
    "refactor: moved nothing to a different place",
    "perf: optimized the art of doing nothing",
    "chore: kept the commit graph employed",
    "feat: revolutionized absolutely nothing",
    "fix: fixed the fix for the previous fix",
    "docs: added more words to sound productive",
    "test: verified that the nonsense works",
    "feat: implemented commitment issues",
    "perf: productivity remains theoretical",
    "chore: another day another green square",
    "refactor: made the code emotionally stable",
    "feat: pushed the boundaries of pointless",
    "docs: this commit explains itself poorly",
    "fix: the bug was actually a feature",
    "feat: added one more reason to open GitHub",
]


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print(result.stderr.strip() or "Git command failed.")
        raise SystemExit(result.returncode)

    return result.stdout.strip()


def check_ready():
    if not (ROOT / ".git").exists():
        sys.exit("ERROR: Git repository not initialized.")

    if not LOG_FILE.exists():
        sys.exit("ERROR: commit-log.md is missing.")

    if git("status", "--porcelain"):
        sys.exit(
            "ERROR: Working tree is not clean.\n"
            "Commit or stash your existing changes first."
        )

    branch = git("branch", "--show-current")
    if not branch:
        sys.exit("ERROR: No branch is checked out.")

    print(f"Repository: {ROOT.name}")
    print(f"Branch: {branch}")


def make_commit():
    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )
    message = random.choice(MESSAGES)

    entry = (
        f"\n- [{timestamp}] {message}\n"
    )

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(entry)

    git("add", "commit-log.md")

    try:
        git("commit", "-m", message)
    except SystemExit:
        # Keep the working tree clean if the commit fails.
        subprocess.run(
            ["git", "reset", "--", "commit-log.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        raise

    print(f"COMMITTED: {message}")


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  python spam.py daily\n"
            "  python spam.py burst 10"
        )
        return

    mode = sys.argv[1].lower()

    if mode == "daily":
        count = 1
    elif mode == "burst":
        if len(sys.argv) != 3:
            sys.exit("Usage: python spam.py burst 10")

        try:
            count = int(sys.argv[2])
        except ValueError:
            sys.exit("Count must be an integer.")

        if not 1 <= count <= MAX_BURST:
            sys.exit(
                f"Choose a burst between 1 and {MAX_BURST}."
            )
    else:
        sys.exit("Unknown mode. Use daily or burst.")

    check_ready()

    if mode == "burst":
        print(f"\nWARNING: about to create {count} commits.")
        confirm = input("Type YES to continue: ")
        if confirm != "YES":
            print("Burst cancelled. Your graph survives another day.")
            return

    for number in range(count):
        print(f"\n[{number + 1}/{count}]")
        make_commit()

    print(f"\nDone. Created {count} commit(s).")
    print("Nothing has been pushed to GitHub yet.")


if __name__ == "__main__":
    main()
