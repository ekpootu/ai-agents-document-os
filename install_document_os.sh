#!/usr/bin/env bash
# ==============================================================================
# AI Agents Document Operating System (Document OS) - POSIX Installer (Linux/macOS)
# Author: Ekpo Otu, Ph.D. - https://linktr.ee/ekpootu
# ==============================================================================

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv-docos"
PLUGIN_SRC="$SCRIPT_DIR/.agents/plugins/document-os"

echo -e "${CYAN}==========================================================${NC}"
echo -e "${CYAN}    AI Agents Document Operating System (Document OS)     ${NC}"
echo -e "${CYAN}               Linux / macOS Installer                    ${NC}"
echo -e "${CYAN}==========================================================${NC}"

# 1. Check Python
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

echo "[1/4] Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

VENV_PY="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

echo "[2/4] Installing Python dependencies..."
$VENV_PIP install --upgrade pip --quiet
$VENV_PIP install --quiet \
    pypdf pdfplumber pdf2image pdf2docx pytesseract python-docx \
    openpyxl xlsxwriter pandas python-pptx Pillow reportlab

echo "[3/4] Checking system dependencies..."
for tool in soffice pandoc tesseract pdftoppm; do
    if command -v "$tool" &>/dev/null; then
        echo "  - $tool: Installed"
    else
        echo "  - $tool: Missing (Install via apt, dnf, or brew)"
    fi
done

# Optional global deploy
if [ "$1" == "--global" ]; then
    GLOBAL_DIR="$HOME/.gemini/config/plugins/document-os"
    echo "[4/4] Deploying globally to $GLOBAL_DIR..."
    mkdir -p "$GLOBAL_DIR"
    cp -r "$PLUGIN_SRC/"* "$GLOBAL_DIR/"
    echo "Global deployment complete."
fi

echo "Document OS installation complete!"
