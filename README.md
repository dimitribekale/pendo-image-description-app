# Pendo - AI Image Analyzer

A modern desktop application for analyzing images using **free local AI models** with **GPU acceleration**. Perfect for your MacBook Air M2!

## Features

- 🖼️ Drag and drop interface for easy image upload
- 🚀 **M2 GPU acceleration** - Analyze images in 2-5 seconds
- 🤖 Multiple HuggingFace models to choose from
- 🎨 Modern, dark-themed user interface
- 💻 Runs completely offline (after initial model download)
- 🔒 100% private - all processing happens locally
- ⚡ Async processing keeps UI responsive

## Why Pendo?

- **Free Forever**: No API costs, no subscriptions
- **Fast on M2**: Optimized for Apple Silicon GPU
- **Private**: Your images never leave your computer
- **Easy**: Just drag, drop, and analyze

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages (takes 5-10 minutes)
pip install -r requirements.txt
```

### 2. Configure (Optional)

The app works out of the box! But you can customize:

```bash
# Copy example config
cp .env.example .env

# Edit .env to change model (optional)
```

### 3. Run

```bash
python main.py
```

### 4. Use It!

1. Drag and drop any image
2. Click "Analyze Image"
3. Wait 2-5 seconds (with M2 GPU)
4. See detailed AI description

## Available Models

| Model | Quality | Speed (M2) | Size | Best For |
|-------|---------|------------|------|----------|
| **blip-image-captioning-large** | Good | 2-5s | ~1GB | General purpose (default) |
| **blip2-opt-2.7b** | Better | 5-10s | ~5GB | Detailed descriptions |
| **git-large-coco** | Good | 3-6s | ~1.5GB | Object detection |
| **vit-gpt2-image-captioning** | Basic | 1-3s | ~500MB | Quick captions |

To change models, edit `.env`:
```bash
HUGGINGFACE_MODEL=Salesforce/blip2-opt-2.7b
```

## GPU Acceleration

Your M2 chip includes a powerful GPU that makes analysis ~10x faster!

**Check your GPU:**
```bash
python -m src.utils.gpu_check
```

Expected output:
```
✓ Using Apple Silicon (MPS) GPU for inference
Speed: 2-5 seconds per image ⚡
```

**Performance:**
- With M2 GPU: 2-5 seconds ⚡
- Without GPU (CPU): 20-30 seconds 🐌

The app automatically uses your M2 GPU - no configuration needed!

## System Requirements

- **OS**: macOS 12.3+ (for M2 GPU support)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for larger models)
- **Storage**: 2-6GB for models (downloaded once, cached)
- **Internet**: Only for initial model download

## Project Structure

```
pendo/
├── main.py                    # Launch the app
├── requirements.txt           # Dependencies
├── .env.example              # Configuration template
│
├── src/
│   ├── ui/                   # PyQt6 interface
│   │   └── main_window.py   # Main app window
│   ├── services/             # Business logic
│   │   ├── llm_service.py   # HuggingFace integration
│   │   └── image_service.py # Image processing
│   └── utils/                # Utilities
│       ├── gpu_check.py     # GPU detection
│       ├── logger.py        # Logging
│       └── validators.py    # Validation
│
├── config/
│   └── settings.py           # App configuration
│
├── models_cache/             # Downloaded models (auto-created)
├── docs/                     # Documentation
└── tests/                    # Unit tests
```

## Configuration

Edit `.env` file to customize:

```bash
# Model Selection
HUGGINGFACE_MODEL=Salesforce/blip-image-captioning-large

# Device (auto-detects M2 GPU)
HUGGINGFACE_DEVICE=auto  # Options: auto, mps, cpu
```

## Troubleshooting

### Slow Performance?

Check if GPU is being used:
```bash
python -m src.utils.gpu_check
```

Should show "MPS Available: ✅"

If not, ensure:
- macOS 12.3 or later
- PyTorch 2.0+ installed: `pip install --upgrade torch`

### Import Errors?

```bash
pip install -r requirements.txt --force-reinstall
```

### Out of Memory?

Use a smaller model:
```bash
# In .env
HUGGINGFACE_MODEL=nlpconnect/vit-gpt2-image-captioning
```

## Development

Built with:
- **PyQt6** - Cross-platform GUI
- **HuggingFace Transformers** - AI models
- **PyTorch** - Deep learning framework with MPS support
- **Pillow** - Image processing

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[GPU_SUPPORT.md](GPU_SUPPORT.md)** - GPU acceleration details
- **[docs/SETUP.md](docs/SETUP.md)** - Comprehensive setup
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design

## License

MIT

---

**Made for MacBook Air M2** 🚀 | **100% Free & Private** 🔒 | **No API Keys Required** ✨
