#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2025 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import logging
import shutil
from pathlib import Path
from python_builder import MinGWPythonBuilder, BuildConfig


def main():
    parser = argparse.ArgumentParser(description='Python builder command line options')
    parser.add_argument('--repo-root', default='.', help='Repository root directory')
    parser.add_argument('--out-path', default='./out', help='Output directory')
    parser.add_argument('--lldb-py-version', default='3.11.4', help='LLDB Python version')
    parser.add_argument('--lldb-py-detailed-version', default='3.11.4_20250509', help='LLDB Python detailed version')
    parser.add_argument('--mingw-triple', default='x86_64-w64-mingw32', help='MinGW triple')

    args = parser.parse_args()
    build_config = BuildConfig(args)

    # 删除并重新创建 OUT_PATH
    out_path = Path(build_config.OUT_PATH)
    if out_path.exists():
        shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        filename=build_config.OUT_PATH + '/build.log')

    try:
        mingw_builder = MinGWPythonBuilder(build_config)
        mingw_builder.build()
        mingw_builder.prepare_for_package()
        mingw_builder.package()
        logging.info("MinGW Python 构建、准备和打包完成。")
    except Exception as e:
        logging.error(f"MinGW 构建过程中发生错误: {str(e)}")


if __name__ == "__main__":
    main()
