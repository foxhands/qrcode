# QR Code Generator & Decoder

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)](#)

A powerful Python script that creates QR codes from text input and displays them directly in your terminal. The script also generates high-quality PNG images and supports QR code decoding from image files.

## ✨ Features

- 🖥️ **Terminal Display** - View QR codes directly in your command line
- 💾 **High-Quality Images** - Generate PNG files with customizable scaling
- 🔍 **QR Code Decoding** - Read and decode existing QR code images
- 🎨 **Colorized Output** - Beautiful colored terminal interface
- 📁 **Auto Directory Creation** - Automatically creates output directories
- ⚡ **Cross-Platform** - Works on Windows and Linux
- 🔧 **Multiple Input Methods** - Interactive mode or command-line arguments

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Git (for cloning)

### Installation

#### Linux/Ubuntu
```bash
# Install system dependencies
sudo apt install git python3 python3-pip zbar-tools

# Clone the repository
git clone https://github.com/foxhands/qrcode.git
cd qrcode

# Install Python dependencies
pip3 install -r requirements.txt

# Make script executable
chmod +x qrgenerator.py
```

#### Windows
```cmd
# Clone the repository
git clone https://github.com/foxhands/qrcode.git
cd qrcode

# Install Python dependencies
pip install -r requirements.txt
```

### Verify Installation
```bash
# Check if Git and Python are installed
git --version
python3 --version  # or python --version on Windows
```

## 📖 Usage

### Interactive Mode
Simply run the script without arguments for an interactive experience:

```bash
./qrgenerator.py
# or on Windows:
python qrgenerator.py
```

### Command Line Arguments

#### Generate QR Code with Text Input
```bash
# Basic usage - auto-generated filename
./qrgenerator.py -i "Your text here"

# Custom filename
./qrgenerator.py -i "Your text here" -o "my_qr_code"
```

#### Decode QR Code from Image
```bash
./qrgenerator.py -d "path/to/qrcode.png"
```

### Examples

```bash
# Create QR code for a URL
./qrgenerator.py -i "https://github.com/foxhands/qrcode" -o "github_repo"

# Create QR code for contact info
./qrgenerator.py -i "Contact: +1234567890" -o "contact"

# Decode an existing QR code
./qrgenerator.py -d "qrcodes/my_qr_code.png"
```

## 📁 Project Structure

```
qrcode/
├── qrgenerator.py      # Main script
├── banner.py           # Banner display module
├── requirements.txt    # Python dependencies
├── qrcodes/           # Generated QR code images (auto-created)
└── README.md          # This file
```

## 🛠️ Dependencies

The script requires the following Python packages:

- `pyqrcode` - QR code generation
- `pypng` - PNG image creation
- `pyzbar` - QR code decoding
- `Pillow` - Image processing
- `colorama` - Terminal colors
- `pyyaml` - YAML parsing
- `isort` - Import sorting

## 🔧 Configuration

### Output Directory
QR code images are saved in the `qrcodes/` directory, which is automatically created if it doesn't exist.

### Image Quality
The script generates high-quality PNG images with a scale factor of 10 for optimal clarity.

## 🐛 Troubleshooting

### Common Issues

#### Windows Filename Error
If you encounter `OSError: [Errno 22] Invalid argument` on Windows, this is due to invalid characters in filenames. The latest version fixes this issue by using Windows-compatible datetime formatting.

#### Missing Modules
If you see "Install missing modules" error, run:
```bash
pip install -r requirements.txt
```

#### Permission Issues (Linux)
Make the script executable:
```bash
chmod +x qrgenerator.py
```

## 📝 Recent Updates

- ✅ Fixed Windows filename compatibility issue
- ✅ Improved error handling
- ✅ Enhanced cross-platform support
- ✅ Added colored terminal output

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**foxhands**
- GitHub: [@foxhands](https://github.com/foxhands)

## 🙏 Acknowledgments

- Original concept inspired by QR code generation needs
- Thanks to the Python community for excellent libraries
- Special thanks to contributors and users providing feedback

---

⭐ **Star this repository if you find it useful!**
