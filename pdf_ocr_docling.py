"""
PDF一括OCR処理ツール (Docling版)

変更点 (v2):
 1) 処理モードの選択を廃止し、常に「詳細モード（構造保持）」で抽出
 2) PDFファイルごとの出力に加えて、全PDFの抽出結果を連結したファイルも出力

Doclingを使用してPDFからテキストを抽出します。
"""

import sys
import time
from pathlib import Path
from typing import List, Tuple, Optional


def check_dependencies() -> bool:
    """必要なライブラリがインストールされているか確認"""
    missing = []

    try:
        import docling  # noqa: F401
    except ImportError:
        missing.append("docling")

    # doclingの中のクラスが読めるかも確認
    try:
        from docling.document_converter import DocumentConverter  # noqa: F401
    except Exception:
        if "docling" not in missing:
            missing.append("docling")

    if missing:
        print("\n" + "=" * 60)
        print("エラー: 必要なライブラリがインストールされていません")
        print("=" * 60)
        print(f"\n不足しているライブラリ: {', '.join(sorted(set(missing)))}")
        print("\nインストールコマンド:")
        print("  pip install docling")
        print("\n注意: Doclingのインストールには時間がかかる場合があります")
        print("=" * 60)
        return False

    return True


def process_pdf_detailed(pdf_path: Path, output_dir: Path) -> Tuple[bool, str]:
    """詳細なテキスト抽出（表や構造を保持）。

    Returns:
        (success, markdown_text)
    """
    from docling.document_converter import DocumentConverter

    pdf_name = pdf_path.stem
    output_path = output_dir / f"{pdf_name}_ocr.txt"
    output_json_path = output_dir / f"{pdf_name}_structure.json"

    print(f"\n処理中: {pdf_path.name}")

    try:
        print(" Doclingでドキュメントを解析中...")
        converter = DocumentConverter()
        result = converter.convert(str(pdf_path))

        # マークダウン形式でテキストを取得
        markdown_text = result.document.export_to_markdown()

        # テキストファイルに保存（マークダウン形式）
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"ファイル: {pdf_path.name}\n")
            f.write("処理モード: 詳細モード（構造保持）\n")
            f.write("=" * 60 + "\n\n")
            f.write(markdown_text)

        # 構造情報をJSONで保存（失敗しても本処理は継続）
        try:
            import json

            json_data = result.document.export_to_dict()
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f" ✓ 構造情報を保存: {output_json_path.name}")
        except Exception as json_error:
            print(f" ⚠ 構造情報の保存に失敗: {json_error}")

        print(f" ✓ 完了: {output_path.name}")
        return True, markdown_text

    except Exception as e:
        print(f" ✗ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False, ""


def write_concatenated_output(
    pdf_files: List[Path], output_dir: Path, markdown_texts: List[str]
) -> Path:
    """全PDFの抽出結果を連結したテキストファイルを作成"""
    combined_path = output_dir / "combined_ocr.txt"

    with open(combined_path, "w", encoding="utf-8") as f:
        for pdf_path, md in zip(pdf_files, markdown_texts):
            f.write("=" * 60 + "\n")
            f.write(f"ファイル: {pdf_path.name}\n")
            f.write("処理モード: 詳細モード（構造保持）\n")
            f.write("=" * 60 + "\n\n")
            f.write(md)
            f.write("\n\n")

    return combined_path


def batch_process_pdfs(pdf_files: List[Path], output_dir: Path):
    """複数のPDFファイルを一括処理（常に詳細モード）"""
    success_count = 0
    failed_files = []
    markdown_texts: List[str] = []

    start_time = time.time()

    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}]")
        success, md = process_pdf_detailed(pdf_file, output_dir)
        if success:
            success_count += 1
            markdown_texts.append(md)
        else:
            failed_files.append(pdf_file.name)
            markdown_texts.append("")

    elapsed_time = time.time() - start_time

    # 連結ファイルを出力（成功した分だけ連結する）
    successful_pairs = [(p, m) for p, m in zip(pdf_files, markdown_texts) if m]
    combined_path: Optional[Path] = None
    if successful_pairs:
        combined_path = write_concatenated_output(
            [p for p, _ in successful_pairs],
            output_dir,
            [m for _, m in successful_pairs],
        )

    return success_count, failed_files, elapsed_time, combined_path


def main() -> None:
    """メイン処理"""
    print("=" * 60)
    print("PDF一括OCR処理ツール (Docling版) - 詳細モード固定")
    print("=" * 60)
    print()
    print("Doclingの特徴:")
    print(" - Popplerのインストール不要")
    print(" - OCR言語パックのインストール不要")
    print(" - 表や構造を保持した抽出が可能")
    print(" - 複数のドキュメント形式に対応")
    print()

    # 依存関係チェック
    if not check_dependencies():
        input("\nEnterキーを押して終了...")
        sys.exit(1)

    # Doclingのバージョン表示
    try:
        import docling
        print(f"Docling バージョン: {docling.__version__}")
    except Exception:
        pass

    # フォルダパスの入力
    if len(sys.argv) > 1:
        input_path = sys.argv[1].strip('"')
    else:
        print("\nPDFファイルまたはフォルダのパスを入力してください:")
        input_path = input("> ").strip('"')

    input_path = Path(input_path)

    if not input_path.exists():
        print(f"\nエラー: パスが見つかりません: {input_path}")
        input("\nEnterキーを押して終了...")
        sys.exit(1)

    # PDFファイルのリストを取得
    if input_path.is_file():
        if input_path.suffix.lower() != ".pdf":
            print(f"\nエラー: PDFファイルではありません: {input_path}")
            input("\nEnterキーを押して終了...")
            sys.exit(1)

        pdf_files = [input_path]
        output_dir = input_path.parent / "ocr_output"
    else:
        pdf_files = sorted(input_path.glob("*.pdf"))
        output_dir = input_path / "ocr_output"

    if not pdf_files:
        print(f"\nエラー: PDFファイルが見つかりません: {input_path}")
        input("\nEnterキーを押して終了...")
        sys.exit(1)

    print(f"\n見つかったPDFファイル: {len(pdf_files)}件")

    # 出力フォルダ作成
    output_dir.mkdir(exist_ok=True)

    print(f"\n出力フォルダ: {output_dir}")
    print("処理モード: 詳細モード（構造保持）")
    print("\n処理を開始します...")

    # バッチ処理
    success_count, failed_files, elapsed_time, combined_path = batch_process_pdfs(pdf_files, output_dir)

    # 結果表示
    print("\n" + "=" * 60)
    print("処理完了")
    print("=" * 60)
    print(f"成功: {success_count}/{len(pdf_files)}")

    if failed_files:
        print(f"失敗: {len(failed_files)}件")
        print("失敗したファイル:")
        for filename in failed_files:
            print(f" - {filename}")

    if combined_path:
        print(f"連結ファイル: {combined_path.name}")

    print(f"処理時間: {elapsed_time:.1f}秒")
    print(f"出力先: {output_dir}")
    print("=" * 60)

    input("\nEnterキーを押して終了...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n処理を中断しました")
        sys.exit(0)
    except Exception as e:
        print(f"\n予期しないエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        input("\nEnterキーを押して終了...")
        sys.exit(1)