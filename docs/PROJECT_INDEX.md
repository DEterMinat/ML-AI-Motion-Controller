# 🎮 Motion Controller - Project Index

## 📁 Project Files Overview

### 🚀 Getting Started (Start Here!)
- **QUICKSTART.md** - 5-minute setup guide (READ THIS FIRST)
- **README.md** - Complete project overview and workflow
- **setup.bat** - Automatic environment setup for Windows (DOUBLE-CLICK TO RUN)

### 📚 Documentation
- **DOCUMENTATION.md** - Comprehensive technical documentation
- **requirements.txt** - Python package dependencies

### 🐍 Python Scripts (The Main Code)

#### 1️⃣ **data_collector.py** - Data Collection
**Purpose**: Capture training data from your webcam  
**When to use**: Phase 1 of the workflow  
**Run**: `python data_collector.py`

**What it does**:
- Opens your webcam
- Shows real-time pose visualization
- Saves pose landmarks to CSV file
- Requires you to press 's' to save frames

**Input**: Keyboard input (label name)  
**Output**: `boxing_data.csv` (training dataset)

---

#### 2️⃣ **train_model.py** - Model Training
**Purpose**: Train a machine learning classifier  
**When to use**: Phase 2 of the workflow  
**Run**: `python train_model.py`

**What it does**:
- Loads data from CSV
- Splits into training/testing sets
- Trains Random Forest classifier
- Evaluates model accuracy
- Saves trained model files

**Input**: `boxing_data.csv`  
**Output**: `boxing_model.pkl`, `label_encoder.pkl`

---

#### 3️⃣ **main.py** - Game Controller
**Purpose**: Real-time punch detection and game input  
**When to use**: Phase 3 of the workflow  
**Run**: `python main.py`

**What it does**:
- Loads trained model
- Processes webcam frames
- Detects punches in real-time
- Sends clicks to Roblox game
- Shows confidence scores on screen

**Input**: Webcam feed  
**Output**: Game input (mouse clicks)

---

#### 4️⃣ **setup_helper.py** - Environment Verification
**Purpose**: Verify or install Python packages  
**When to use**: If packages are missing  
**Run**: `python setup_helper.py`

**What it does**:
- Checks Python version
- Verifies installed packages
- Can install missing packages via pip

---

### ⚙️ Configuration Files

#### conda-environment.yml
- **Purpose**: Conda environment specification
- **Use**: `conda env create -f conda-environment.yml`
- **Contains**: Python 3.10 + all dependencies

#### requirements.txt
- **Purpose**: pip package list
- **Use**: `pip install -r requirements.txt`
- **Contains**: All Python package versions

#### setup.bat
- **Purpose**: Windows batch script
- **Use**: Double-click to run
- **What it does**: Automatic Conda environment setup

---

## 🔄 Workflow at a Glance

```
START HERE
    ↓
[QUICKSTART.md or setup.bat]
    ↓
Install Python & Conda
    ↓
Create environment
    ↓
Install dependencies
    ↓
┌─────────────────────────────────────────┐
│ PHASE 1: Collect Training Data          │
│ Run: python data_collector.py           │
│ Time: 1-2 hours                         │
│ Output: boxing_data.csv                 │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ PHASE 2: Train Model                    │
│ Run: python train_model.py              │
│ Time: 1-2 minutes                       │
│ Output: boxing_model.pkl               │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ PHASE 3: Play Game!                     │
│ Run: python main.py                     │
│ Time: As long as you want               │
│ Control: Punch movements                │
└─────────────────────────────────────────┘
```

---

## 📖 How to Use This Documentation

### If you're new to this project:
1. **First**: Read `QUICKSTART.md` (5 min read)
2. **Then**: Run `setup.bat` (automatic setup)
3. **Next**: Follow the 3-phase workflow
4. **Reference**: Check `README.md` for details

### If you need detailed information:
- **General questions**: `README.md`
- **Installation help**: `DOCUMENTATION.md` → Installation section
- **Troubleshooting**: `DOCUMENTATION.md` → Troubleshooting section
- **Technical details**: `DOCUMENTATION.md` → Technical Details section

### If you want to modify the system:
- **Changing inputs**: Edit `main.py` → `trigger_game_action()`
- **Adding new actions**: `DOCUMENTATION.md` → Advanced Topics
- **Tuning thresholds**: `main.py` → `CONFIDENCE_THRESHOLD`, `COOLDOWN_DURATION`
- **Different classifier**: `train_model.py` → Change model class

### If something goes wrong:
1. Check console error message
2. Find error type in `DOCUMENTATION.md` → Troubleshooting
3. Follow suggested solutions
4. Run `setup_helper.py` to verify installation
5. Check `README.md` → Troubleshooting section

---

## 🎯 Key Concepts

### Three Main Files (The Code You'll Run)

| File | Purpose | Phase | Time |
|------|---------|-------|------|
| data_collector.py | Capture training data | 1 | 1-2 hrs |
| train_model.py | Train classifier | 2 | 1-2 min |
| main.py | Real-time control | 3 | Ongoing |

### Three Generated Files (Automatically Created)

| File | Created By | Used By | Purpose |
|------|-----------|---------|---------|
| boxing_data.csv | data_collector | train_model | Training dataset |
| boxing_model.pkl | train_model | main | Trained classifier |
| label_encoder.pkl | train_model | main | Label mapping |

### Four Configuration Files (Setup/Reference)

| File | Purpose | Type |
|------|---------|------|
| conda-environment.yml | Environment spec | Conda |
| requirements.txt | Package list | pip |
| setup.bat | Auto setup | Batch script |
| setup_helper.py | Verify packages | Python |

### Four Documentation Files (Read These!)

| File | Best For | Length |
|------|----------|--------|
| QUICKSTART.md | Getting started | 2 pages |
| README.md | Overview & workflow | 5 pages |
| DOCUMENTATION.md | Complete reference | 20+ pages |
| PROJECT_INDEX.md | This file | Navigation |

---

## 🚀 Quick Commands

### Setup (One-time)
```bash
# Option A: Windows (easiest)
setup.bat

# Option B: Conda (all platforms)
conda env create -f conda-environment.yml
conda activate motion-controller

# Option C: pip (minimal)
pip install -r requirements.txt
```

### Phase 1: Collect Data
```bash
python data_collector.py
# Press 's' to save, 'q' to quit
```

### Phase 2: Train Model
```bash
python train_model.py
# Check accuracy (aim for > 0.85)
```

### Phase 3: Play!
```bash
python main.py
# Perform punches, watch game respond
```

### Troubleshoot
```bash
python setup_helper.py
# Verify all packages installed
```

---

## 📊 File Dependency Graph

```
setup.bat / conda-environment.yml / requirements.txt
    ↓
    ↓ (installs)
    ↓
data_collector.py ──────→ boxing_data.csv
                              ↓
                         train_model.py ──→ boxing_model.pkl
                                       ↓   label_encoder.pkl
                                       ↓
                                    main.py ──→ Game Input
                                              (mouse clicks)
```

---

## ✅ Success Checklist

- [ ] Downloaded and installed Conda/Miniconda
- [ ] Ran `setup.bat` or created environment manually
- [ ] Verified installation with `setup_helper.py`
- [ ] Ran `data_collector.py` and collected 100+ samples
- [ ] Ran `train_model.py` and achieved > 0.85 accuracy
- [ ] Ran `main.py` and tested punches in game
- [ ] Adjusted `CONFIDENCE_THRESHOLD` if needed
- [ ] Can reliably control game with punches

---

## 🎓 Learning Path

If you want to understand the code:

1. **Python Basics**: Variables, functions, loops
2. **OpenCV**: Reading video frames, image processing
3. **MediaPipe**: Pose detection landmarks
4. **Pandas**: Loading and manipulating data
5. **scikit-learn**: Training classifiers
6. **PyDirectInput**: Keyboard/mouse automation

Each script builds on these concepts progressively:
- `data_collector.py`: OpenCV + MediaPipe
- `train_model.py`: Pandas + scikit-learn
- `main.py`: All of the above + PyDirectInput

---

## 💡 Tips for Success

1. **Good Lighting**: Most important factor for pose detection
2. **Diverse Training Data**: Vary angles, distances, speeds
3. **Clear Distinction**: Make neutral and punch poses obviously different
4. **Proper Distance**: Stand 2-3 meters from camera
5. **Test Incrementally**: Don't skip phases or jump ahead
6. **Monitor Accuracy**: Aim for > 90% for reliable control
7. **Adjust Thresholds**: Fine-tune based on actual gameplay
8. **Keep Experimenting**: Try different data, poses, and settings

---

## 🆘 Getting Help

### Problem-Solving Steps
1. Read error message carefully
2. Search in `DOCUMENTATION.md` Troubleshooting
3. Check `README.md` → Troubleshooting
4. Run `setup_helper.py` to verify setup
5. Check console output for clues

### Common Issues Quick Links
- **Conda not found**: DOCUMENTATION.md → Installation Issues
- **Pose not detected**: DOCUMENTATION.md → Webcam Issues
- **Low accuracy**: README.md → Troubleshooting
- **Game not responding**: DOCUMENTATION.md → Runtime Issues

---

## 📈 Next Steps After Success

### Improve Performance
- Collect more training data
- Try different ML algorithms
- Tune hyperparameters
- Reduce frame latency

### Add Features
- Add more action classes
- Use hand detection
- Add temporal features
- Implement combo moves

### Customize for Other Games
- Change input mappings
- Add different gestures
- Combine multiple inputs
- Create game-specific profiles

---

## 📞 Quick Reference

### Files by Purpose

**Want to collect data?**  
→ Use `data_collector.py`

**Want to train model?**  
→ Use `train_model.py`

**Want to control game?**  
→ Use `main.py`

**Setup problems?**  
→ Use `setup.bat` or `setup_helper.py`

**Need to understand something?**  
→ Check `DOCUMENTATION.md`

**In a hurry?**  
→ Read `QUICKSTART.md`

---

## 🎉 You're All Set!

Everything you need is here. Start with `QUICKSTART.md` and follow the workflow. Good luck! 👊🎮

---

**Last Updated**: December 2025  
**Project Version**: 1.0  
**Status**: ✅ Production Ready

For the most detailed guide, see **DOCUMENTATION.md**.  
For the fastest setup, run **setup.bat** or read **QUICKSTART.md**.
