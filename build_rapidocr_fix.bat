@echo off
REM PDF OCR Tool - rapidocr（統合版）対応ビルドスクリプト

echo ============================================================
echo PDF OCR Tool - PyInstaller ビルド (rapidocr版)
echo ============================================================
echo.

set VENV_NAME=venv

if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo [エラー] 仮想環境が見つかりません: %VENV_NAME%
    pause
    exit /b 1
)

echo 仮想環境を有効化: %VENV_NAME%
call %VENV_NAME%\Scripts\activate.bat
echo.

echo [確認] インストール済みパッケージ
python --version
pip show rapidocr
echo.

echo [1/3] クリーンアップ中...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist pdf_ocr.spec del pdf_ocr.spec

echo.
echo [2/3] PyInstallerでexeファイルをビルド中...
echo       この処理には数分かかります...
echo.

python -m PyInstaller ^
  --clean ^
  --name pdf_ocr ^
  --onefile ^
  --console ^
  --collect-all docling ^
  --collect-all docling_core ^
  --collect-all docling_ibm_models ^
  --collect-all docling_parse ^
  --collect-all rapidocr ^
  --collect-data rapidocr ^
  --collect-all pdfplumber ^
  --collect-all pypdf ^
  --collect-all PIL ^
  --collect-all cv2 ^
  --collect-data docling ^
  --collect-data docling_core ^
  --collect-data docling_ibm_models ^
  --copy-metadata docling ^
  --copy-metadata docling-core ^
  --copy-metadata docling-ibm-models ^
  --copy-metadata docling-parse ^
  --copy-metadata rapidocr ^
  --hidden-import docling.document_converter ^
  --hidden-import docling.datamodel.base_models ^
  --hidden-import docling.datamodel.document ^
  --hidden-import docling.backend.pypdfium2_backend ^
  --hidden-import docling.backend.docling_parse_backend ^
  --hidden-import docling_core ^
  --hidden-import docling_ibm_models ^
  --hidden-import docling_parse ^
  --hidden-import rapidocr ^
  --hidden-import rapidocr.main ^
  --hidden-import rapidocr.ch_ppocr_rec ^
  --hidden-import rapidocr.ch_ppocr_det ^
  --hidden-import rapidocr.cal_rec_boxes ^
  --hidden-import rapidocr.inference_engine ^
  --hidden-import rapidocr.inference_engine.base ^
  --hidden-import pdfplumber ^
  --hidden-import pypdf ^
  --hidden-import PIL ^
  --hidden-import cv2 ^
  --hidden-import numpy ^
  --hidden-import onnxruntime ^
  --hidden-import omegaconf ^
  --hidden-import yaml ^
  pdf_ocr_docling.py

if errorlevel 1 (
    echo.
    echo [エラー] ビルドに失敗しました
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] ビルド完了
echo.
echo 出力先: dist\pdf_ocr.exe
echo.
echo ============================================================
echo 注意事項
echo ============================================================
echo.
echo - exeファイルのサイズが大きくなります（500MB～1GB程度）
echo - これはrapicocrのOCRモデルファイルを含むためです
echo - 初回実行時は解凍に時間がかかる場合があります
echo.
echo ============================================================
echo ビルド完了！
echo ============================================================
echo.
pause