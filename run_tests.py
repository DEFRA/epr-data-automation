import sys, argparse, subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keyword", default=None, help="pytest -k expression")
    parser.add_argument("extra", nargs="*", help="extra pytest args")
    args = parser.parse_args()

    cmd = ["pytest", "-c", "config/pytest.ini"]
    if args.keyword:
        cmd += ["-k", args.keyword]
    cmd += args.extra
    raise SystemExit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
