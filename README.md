# Real-time Hand Gesture-Based HCI System

This is a real-time **Human-Computer Interaction (HCI)** project that enables users to control **system volume** and **screen brightness** using **hand gestures** captured via webcam. The system uses fingertip tracking and gesture recognition to create a contactless interface.

Engineered using **Python**, **OpenCV**, **MediaPipe**, and Windows APIs (`pycaw` for volume and `wmi` for brightness), this application enhances accessibility and user interaction with intuitive, real-time visual feedback.


---

##  Features

-  Real-time hand detection and tracking using **MediaPipe**
-  Finger state recognition (e.g., thumb-index distance)
-  Volume control via hand gesture (with safety trigger: pinky down)
-  Screen brightness control via hand gesture
-  On-screen visual feedback and FPS display
-  Modular design with a reusable hand tracking module


---

##  Project Structure
```bash
RealTime-HandGesture-HCI/
├── handtrackingmodule.py # Core reusable module for hand tracking
├── VolumeHandControl.py # Controls system volume via gestures
├── GestureBrightnessControl.py # Controls screen brightness via gestures
├── requirements.txt # All required Python packages
├── .gitignore # Prevents upload of unnecessary files
└── README.md # Project documentation (this file)
```
---

##  Install Dependencies

Install all required Python libraries:

```bash
pip install -r requirements.txt
```

## Or install manually:
```bash
pip install opencv-python mediapipe numpy pycaw wmi comtypes
```


##  How to Run

###  Volume Control
```bash
python VolumeHandControl.py
```
## Brightness Control
```bash
python GestureBrightnessControl.py
```
 Use a pinch gesture (thumb + index finger) to adjust settings.
 Setting is only applied when pinky is down (gesture safety mechanism).

##  Technologies Used

| Library      | Purpose                            |
|--------------|-------------------------------------|
| OpenCV       | Webcam image capture and drawing    |
| MediaPipe    | Hand detection and landmark tracking |
| Numpy        | Interpolation and calculations      |
| Pycaw        | Control system volume (Windows)     |
| WMI          | Control brightness (Windows)        |
| comtypes     | Windows COM support for Pycaw       |


---

##  Academic Relevance

This project was developed as part of a **Computer Vision** academic module, with practical applications in gesture-based user interfaces, accessibility tools, and touchless computing systems.

---

##  Author

**Mohd Saif**  
 Master’s Student – Colorado State University  
 GitHub: [mohdsaifcsu](https://github.com/mohdsaifcsu)

---

##  License

This project is released for **educational and academic purposes only**.  
Please cite or credit appropriately if used in your work.

---

##  Future Work

- Add gesture-controlled media playback
- Support cross-platform brightness control
- Extend to smart home IoT integration (light/sound control)
- Deploy web-based interface using Flask or Streamlit
