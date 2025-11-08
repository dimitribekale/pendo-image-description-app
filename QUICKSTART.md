# Quick Start - Pendo Image Analyzer

Get your free AI image analyzer running in 5 minutes on your MacBook Air M2!

## Installation (3 Simple Steps)

### 1. Install Dependencies

```bash
# Navigate to project
cd pendo-image-description-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages (takes 5-10 minutes due to PyTorch size)
pip install -r requirements.txt
```

### 2. Run the App

```bash
python main.py
```

That's it! No API keys, no configuration needed.

### 3. Analyze Your First Image

1. **Drag & Drop**: Drop any image onto the window
2. **Click Analyze**: Press the blue "Analyze Image" button
3. **Wait 2-5 seconds**: Your M2 GPU will process it
4. **See Results**: AI description appears on the right

## First Run

The first time you analyze an image:
- The AI model downloads (~1GB)
- Takes about 2-3 minutes
- Models are cached for future use
- Only happens once!

## Performance

**On your MacBook Air M2:**
- First image: ~3 minutes (downloading model)
- All subsequent images: **2-5 seconds** ⚡
- Uses your M2 GPU automatically
- 10x faster than CPU mode

## Verify GPU is Working

```bash
python -m src.utils.gpu_check
```

Should show:
```
✓ Using Apple Silicon (MPS) GPU for inference
```

## Change AI Model (Optional)

Want better quality or faster speed?

```bash
# Copy config file
cp .env.example .env

# Edit .env and change model:
# For better quality (slower, 5GB):
HUGGINGFACE_MODEL=Salesforce/blip2-opt-2.7b

# For faster speed (lighter, 500MB):
HUGGINGFACE_MODEL=nlpconnect/vit-gpt2-image-captioning
```

## Troubleshooting

### "No module named 'torch'"
```bash
pip install -r requirements.txt
```

### Slow performance?
```bash
# Check if M2 GPU is being used
python -m src.utils.gpu_check

# Should say "MPS Available: ✅"
# If not, update PyTorch:
pip install --upgrade torch torchvision
```

### Out of memory?
Use lighter model:
```bash
# In .env file
HUGGINGFACE_MODEL=nlpconnect/vit-gpt2-image-captioning
```

## What's Next?

- Try different images to see AI descriptions
- Switch between models to compare quality
- Read [README.md](README.md) for more features
- Check [GPU_SUPPORT.md](GPU_SUPPORT.md) for optimization tips

## Available Models

| Model | Quality | Speed | Size |
|-------|---------|-------|------|
| blip-image-captioning-large | ⭐⭐⭐ | 2-5s | 1GB (default) |
| blip2-opt-2.7b | ⭐⭐⭐⭐ | 5-10s | 5GB |
| git-large-coco | ⭐⭐⭐ | 3-6s | 1.5GB |
| vit-gpt2-image-captioning | ⭐⭐ | 1-3s | 500MB |

## Key Features

- ✅ **Free Forever** - No API costs
- ✅ **M2 Optimized** - Uses your GPU automatically
- ✅ **Private** - All processing on your Mac
- ✅ **Offline** - Works without internet (after first download)
- ✅ **Easy** - Just drag and drop

---

**Questions?** Check [README.md](README.md) or [docs/SETUP.md](docs/SETUP.md)

**Enjoying Pendo?** Star the repo! ⭐
