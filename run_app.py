import os
import sys
import importlib.metadata

# Streamlit PackageNotFoundError 오류 강제 방지 패치
try:
    importlib.metadata.version("streamlit")
except importlib.metadata.PackageNotFoundError:
    # 메타데이터를 찾지 못할 경우 기본 버전을 강제로 주입
    import importlib.metadata as _im
    _orig_version = _im.version
    def _mock_version(package_name):
        if package_name == "streamlit":
            return "1.30.0"
        return _orig_version(package_name)
    _im.version = _mock_version

import streamlit.web.cli as stcli

if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(__file__), "app.py")
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())