# Quick Start Guide - Motion Controller

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Conda
If you don't have Conda installed:
1. Download **Anaconda** or **Miniconda** from: https://www.anaconda.com/download/
2. Run the installer and follow the instructions
3. Restart your terminal/PowerShell

### Step 2: Setup Environment
Navigate to your Motion Controller folder and run:

#### Windows:
```bash
setup.bat
```

#### macOS/Linux:
```bash
conda env create -f conda-environment.yml
conda activate motion-controller
```

### Step 3: Collect Training Data
```bash
python data_collector.py
```
- Enter action name: `neutral` (or `left_punch`, `right_punch`)
- Press **'s'** to save frames (collect 50-100 per action)
- Press **'q'** to finish
- **Repeat for each action**: `left_punch` and `right_punch`

### Step 4: Train Model
```bash
python train_model.py
```
- Check the accuracy (aim for > 0.85)
- If low, collect more diverse samples

### Step 5: Play!
```bash
python main.py
```
- Focus on your Roblox Boxing Game window
- Perform punches - the game will respond!
- Press **'q'** to quit

---

## 📊 Expected Workflow

```
Data Collection    →    Model Training    →    Game Control
(data_collector)       (train_model)          (main.py)
    ↓                       ↓                      ↓
boxing_data.csv    boxing_model.pkl    Automatic Click Input
```

---

## 🎯 Tips for Best Results

1. **Good Lighting**: Bright, natural lighting works best
2. **Full Body Visible**: Stand so your full body is in frame
3. **Clear Motions**: Punch with deliberate, clear movements
4. **Diverse Samples**: Vary distance, angle, and background
5. **Balanced Data**: Collect similar number of samples per action

---

## ⚙️ Configuration (Optional)

Edit `main.py` to customize:

```python
CONFIDENCE_THRESHOLD = 0.8      # Increase for fewer false positives
COOLDOWN_DURATION = 0.5         # Increase to reduce spam clicks
```

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Conda not found | Install from https://www.anaconda.com/download/ |
| Webcam not working | Check Windows Settings > Privacy > Camera |
| Low accuracy | Collect more diverse training data |
| Game not responding | Ensure Roblox window is focused, check confidence score |
| Too many false clicks | Increase CONFIDENCE_THRESHOLD or COOLDOWN_DURATION |

---

## 📚 Project Files

- **data_collector.py** - Capture training data
- **train_model.py** - Train classification model
- **main.py** - Real-time game controller
- **boxing_data.csv** - Your training dataset
- **boxing_model.pkl** - Trained model
- **label_encoder.pkl** - Label encoding

---

## 🎮 Game Input

The controller sends:
- **Left Punch**: Left mouse click
- **Right Punch**: Right mouse click
- **Neutral**: No input

You can modify these in `main.py`'s `trigger_game_action()` function.

---

Enjoy! 👊🎮
