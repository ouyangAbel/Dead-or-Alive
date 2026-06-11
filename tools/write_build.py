# -*- coding: utf-8 -*-
from pathlib import Path
import base64
code = base64.b64decode(Path("tools/build_guides.b64").read_text(encoding="ascii")).decode("utf-8")
Path("tools/build_guides.py").write_text(code, encoding="utf-8")
print("decoded", len(code))

