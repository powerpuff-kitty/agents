from pathlib import Path
for number, line in enumerate(Path("request.log").read_text().splitlines(), 1):
    print(str(number) + ": " + (line.split("authorization=", 1)[0] + "authorization=[REDACTED]" if "authorization=" in line else line))
