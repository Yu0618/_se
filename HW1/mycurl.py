#!/usr/bin/env python3
"""
mycurl - 一個簡易的類 curl 命令列 HTTP 用戶端工具
需求套件: pip install requests
"""

import argparse
import json
import sys
import requests


def parse_headers(header_list):
    """解析 -H / --header 傳入的標頭格式 (e.g., 'Content-Type: application/json')"""
    headers = {}
    if not header_list:
        return headers

    for h in header_list:
        if ":" in h:
            key, value = h.split(":", 1)
            headers[key.strip()] = value.strip()
        else:
            print(f"Warning: 無法解析標頭格式 '{h}'，忽視該設定。", file=sys.stderr)
    return headers


def main():
    parser = argparse.ArgumentParser(
        description="mycurl - 一個簡易的類 curl HTTP 請求工具",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # 位置參數：目標 URL
    parser.add_argument("url", help="目標 URL (例如: https://httpbin.org/get)")

    # HTTP 方法
    parser.add_argument(
        "-X",
        "--request",
        default="GET",
        metavar="METHOD",
        help="指定 HTTP 請求方法 (預設: GET)",
    )

    # 標頭設定
    parser.add_argument(
        "-H",
        "--header",
        action="append",
        metavar="HEADER",
        help="加入 HTTP Header (可重複使用，如 -H 'Accept: application/json')",
    )

    # 請求資料 (Data / JSON)
    parser.add_argument(
        "-d",
        "--data",
        metavar="DATA",
        help="傳送 HTTP POST Data (字串或 Raw Data)",
    )
    parser.add_argument(
        "--json",
        metavar="JSON_STRING",
        help="傳送 JSON 格式資料 (會自動設定 Content-Type: application/json)",
    )

    # 輸出與 HTTP 標頭顯示
    parser.add_argument(
        "-i",
        "--include",
        action="store_true",
        help="在輸出結果中包含 HTTP 回應 Header",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="將回應 Body 寫入指定的檔案而非標準輸出",
    )

    # 行為控制
    parser.add_argument(
        "-L",
        "--location",
        action="store_true",
        help="自動跟隨 HTTP 重定向 (Redirect)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        metavar="SECONDS",
        help="請求超時時間 (秒，預設: 30)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="顯示詳細的發送與接收過程 (Verbose mode)",
    )

    args = parser.parse_args()

    # 處理 Headers
    headers = parse_headers(args.header)

    # 處理 Data 與 JSON
    data_to_send = None
    json_to_send = None

    if args.json:
        try:
            json_to_send = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"Error: 無法解析傳入的 JSON 字串: {e}", file=sys.stderr)
            sys.exit(1)
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
    elif args.data:
        data_to_send = args.data
        # 如果使用者指定 -d 但沒有指定方法，預設提升為 POST
        if args.request == "GET":
            args.request = "POST"

    # Verbose 模式輸出請求資訊
    if args.verbose:
        print(f"> {args.request.upper()} {args.url}", file=sys.stderr)
        for k, v in headers.items():
            print(f"> {k}: {v}", file=sys.stderr)
        print(">", file=sys.stderr)

    # 發起請求
    try:
        response = requests.request(
            method=args.request.upper(),
            url=args.url,
            headers=headers,
            data=data_to_send,
            json=json_to_send,
            allow_redirects=args.location,
            timeout=args.timeout,
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        print(f"Error: 請求失敗 - {e}", file=sys.stderr)
        sys.exit(1)

    # 處理回應 Header 輸出
    header_output = []
    if args.include or args.verbose:
        status_line = f"HTTP/1.1 {response.status_code} {response.reason}"
        if args.verbose:
            print(f"< {status_line}", file=sys.stderr)
            for k, v in response.headers.items():
                print(f"< {k}: {v}", file=sys.stderr)
            print("<", file=sys.stderr)

        if args.include:
            header_output.append(status_line)
            for k, v in response.headers.items():
                header_output.append(f"{k}: {v}")
            header_output.append("\n")

    # 寫入檔案或標準輸出
    if args.output:
        try:
            with open(args.output, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            if args.verbose:
                print(f"* 成功將回應寫入至 {args.output}", file=sys.stderr)
        except IOError as e:
            print(f"Error: 無法寫入檔案 {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if header_output:
            print("\r\n".join(header_output))
        print(response.text)


if __name__ == "__main__":
    main()
