# Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended for local models)
- Internet connection

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pendo-image-description-app
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyQt6 (GUI framework)
- Pillow & OpenCV (image processing)
- Anthropic SDK (Claude API)
- Transformers & PyTorch (HuggingFace models)

**Note:** Installation may take 5-10 minutes due to PyTorch size.

### 4. Configure Your AI Provider

You have two options:

#### Option A: Claude API (Recommended for Best Quality)

1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Create `.env` file in project root:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env`:
   ```
   LLM_PROVIDER=claude
   ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
   CLAUDE_MODEL=claude-3-sonnet-20240229
   ```

#### Option B: HuggingFace Local Models (Free, No API Key)

1. Create `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env`:
   ```
   LLM_PROVIDER=huggingface
   HUGGINGFACE_MODEL=Salesforce/blip-image-captioning-large
   HUGGINGFACE_DEVICE=auto
   ```

### 5. Run the Application

```bash
python main.py
```

## Provider Details

### Claude API Setup

**Sign Up:**
1. Visit https://console.anthropic.com/
2. Create account and add payment method
3. Navigate to API Keys section
4. Create new API key

**Pricing (as of 2024):**
- Claude 3 Haiku: $0.25 per million input tokens (cheapest)
- Claude 3 Sonnet: $3 per million input tokens (balanced)
- Claude 3 Opus: $15 per million input tokens (best quality)

**Estimated cost per image:** $0.001 - $0.01 depending on model and image size

**Available Models:**
```
claude-3-opus-20240229     # Best quality, most expensive
claude-3-sonnet-20240229   # Balanced (default)
claude-3-haiku-20240307    # Fastest, cheapest
```

**Configuration:**
```bash
# In .env file
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-3-sonnet-20240229
```

### HuggingFace Local Models

**No API Key Required!** Models run on your computer.

**First Run:**
- Model will be downloaded automatically (~1-2GB)
- Cached in `models_cache/` directory
- One-time download per model

**System Requirements:**
- CPU mode: 4GB RAM minimum
- GPU mode (CUDA): NVIDIA GPU with 4GB+ VRAM

**Available Models:**

1. **Salesforce/blip-image-captioning-large** (Default)
   - Size: ~990MB
   - Quality: Good
   - Speed: Medium
   - Best for: General purpose

2. **Salesforce/blip2-opt-2.7b**
   - Size: ~5GB
   - Quality: Better
   - Speed: Slower
   - Best for: Detailed descriptions (requires 8GB+ RAM)

3. **microsoft/git-large-coco**
   - Size: ~1.5GB
   - Quality: Good
   - Speed: Medium
   - Best for: Object detection focus

4. **nlpconnect/vit-gpt2-image-captioning**
   - Size: ~500MB
   - Quality: Basic
   - Speed: Fast
   - Best for: Quick captions, low-end hardware

**GPU Acceleration (Recommended):**

The app automatically detects and uses your GPU for much faster inference!

**Check your GPU:**
```bash
# For Apple Silicon (M1/M2/M3)
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"

# For NVIDIA GPU (CUDA)
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

**Device Options:**
- `auto` (recommended) - Automatically uses best available: CUDA > MPS > CPU
- `mps` - Force Apple Silicon GPU (M1/M2/M3 Mac)
- `cuda` - Force NVIDIA GPU
- `cpu` - Force CPU (slowest)

**Speed Comparison on MacBook Air M2:**
- MPS (GPU): ~2-5 seconds per image ⚡
- CPU: ~20-30 seconds per image 🐌

**Configuration:**
```bash
# In .env file
LLM_PROVIDER=huggingface
HUGGINGFACE_MODEL=Salesforce/blip-image-captioning-large
HUGGINGFACE_DEVICE=auto  # Recommended - auto-detects GPU
```

## Troubleshooting

### Qt Platform Plugin Error

**Error**: "Could not find the Qt platform plugin"

**Solution**:
```bash
pip uninstall PyQt6 PyQt6-Qt6
pip install PyQt6
```

### Torch/CUDA Issues

**Error**: "CUDA out of memory"

**Solution**:
- Switch to CPU mode: `HUGGINGFACE_DEVICE=cpu`
- Use smaller model: `nlpconnect/vit-gpt2-image-captioning`
- Close other applications

### Slow HuggingFace Inference

**Solutions**:
- Use GPU if available (30x faster)
- Try lighter model: `nlpconnect/vit-gpt2-image-captioning`
- Consider using Claude API instead

### Claude API Errors

**Error**: "Invalid API key"

**Check**:
1. Key starts with `sk-ant-`
2. No extra spaces in `.env` file
3. Account has billing set up
4. Key has not expired

**Error**: "Rate limit exceeded"

**Solution**:
- Wait a few minutes
- Upgrade your Anthropic plan
- Use HuggingFace instead

### Import Errors

**Error**: "No module named 'PIL'" or similar

**Solution**:
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## Performance Comparison

| Provider | Quality | Speed | Cost | Internet Required |
|----------|---------|-------|------|-------------------|
| Claude Opus | Excellent | 2-5s | $$$ | Yes |
| Claude Sonnet | Very Good | 2-3s | $$ | Yes |
| Claude Haiku | Good | 1-2s | $ | Yes |
| BLIP-large (CPU) | Good | 20-30s | Free | First run only |
| BLIP-large (MPS/M2) | Good | 2-5s | Free | First run only |
| BLIP-large (CUDA) | Good | 2-5s | Free | First run only |
| BLIP2 (MPS/M2) | Better | 5-10s | Free | First run only |
| BLIP2 (CUDA) | Better | 5-10s | Free | First run only |
| ViT-GPT2 (CPU) | Basic | 10-15s | Free | First run only |
| ViT-GPT2 (MPS/M2) | Basic | 1-3s | Free | First run only |

**Note:** MPS = Apple Silicon GPU (M1/M2/M3 MacBooks). GPU inference is ~10x faster than CPU!

## Switching Between Providers

You can easily switch providers by editing `.env`:

```bash
# Switch to Claude
LLM_PROVIDER=claude

# Switch to HuggingFace
LLM_PROVIDER=huggingface

# Switch to Mock (testing)
LLM_PROVIDER=mock
```

No code changes needed - restart the app after editing `.env`

## Next Steps

1. Read [Architecture Guide](ARCHITECTURE.md) for system design
2. Try both providers to compare quality
3. Customize the UI in `config/settings.py`
4. Explore different HuggingFace models

## Getting Help

- Check logs in `logs/` directory
- Review error messages in the UI
- Ensure API keys are properly configured
- Verify internet connection (for Claude/downloads)
