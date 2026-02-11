# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

datas = []
binaries = []
hiddenimports = ['docling.document_converter', 'docling.datamodel.base_models', 'docling.datamodel.document', 'docling.backend.pypdfium2_backend', 'docling.backend.docling_parse_backend', 'docling_core', 'docling_ibm_models', 'docling_parse', 'rapidocr', 'rapidocr.main', 'rapidocr.ch_ppocr_rec', 'rapidocr.ch_ppocr_det', 'rapidocr.cal_rec_boxes', 'rapidocr.inference_engine', 'rapidocr.inference_engine.base', 'pdfplumber', 'pypdf', 'PIL', 'cv2', 'numpy', 'onnxruntime', 'omegaconf', 'yaml']
datas += collect_data_files('rapidocr')
datas += collect_data_files('docling')
datas += collect_data_files('docling_core')
datas += collect_data_files('docling_ibm_models')
datas += copy_metadata('docling')
datas += copy_metadata('docling-core')
datas += copy_metadata('docling-ibm-models')
datas += copy_metadata('docling-parse')
datas += copy_metadata('rapidocr')
tmp_ret = collect_all('docling')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('docling_core')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('docling_ibm_models')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('docling_parse')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('rapidocr')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pdfplumber')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pypdf')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('cv2')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['pdf_ocr_docling.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pdf_ocr',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
