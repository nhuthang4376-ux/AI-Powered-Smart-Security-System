"""
================================================================================
MakeUC 2025 Project: AI-Powered Smart Security System
Team member: Austin Florence, Dang Thai Bao, Vo Nhu Thang
File: final.py
Description:
This script is the central "brain" of our security system. It performs
a complete detect-analyze-alert pipeline:
1.  Listens for a trigger signal from an Arduino-based sensor.
2.  Captures a live image from an IP camera stream.
3.  Sends the image to the Google Gemini AI for analysis.
4.  If a human is confirmed, it generates and plays a local audio
    warning using ElevenLabs.
================================================================================
"""

import time
import platform
import os
from dotenv import load_dotenv

# --- Hardware & Sensor Interface ---
import serial

# --- Video Capture ---
import cv2

# --- AI Analysis ---
from google import genai
from PIL import Image

# --- Audio Alert ---
from elevenlabs.client import ElevenLabs
try:
    # Using playsound3 for cross-platform audio playback
    from playsound3 import playsound
except ImportError:
    print("Warning: 'playsound3' module not found. Audio alerts will be disabled.")
    print("Please run: pip install playsound3")
    playsound = None

# Load environment variables (e.g., GEMINI_API_KEY)
# NOTE: Users must create their own .env file with their GEMINI_API_KEY
load_dotenv()

# ==============================================================================
# --- CONFIGURATION CONSTANTS ---
# ==============================================================================

# NOTE: This IP is for demonstration purposes only.
# To test, please change this to your own IP camera stream URL (e.g., from DroidCam).
IP_CAM_URL = "http://10.11.20.70:4747/video"
# Arduino Serial Port Settings
SERIAL_BAUDRATE = 9600

# NOTE: This API key is for demonstration purposes only and may be inactive.
# To test, please replace this with your own ElevenLabs API key.
ELEVENLABS_API_KEY = "9773d04a0399c0ecfd39c6acd2e43bc6c9145357859a4ec585f2fb5a6b47f588"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Voice: "Rachel"

# ==============================================================================
# --- VIDEO CAPTURE FUNCTION ---
# ==============================================================================

def capture_image_from_ipcam(url):
    """
    Captures a single frame from the specified IP camera stream.
    
    Args:
        url (str): The video stream URL from the IP camera.
    
    Returns:
        str or None: The file path of the saved image ("snapshot.jpg")
                     or None if capture failed.
    """
    print(f"[Video]: Connecting to IP Cam at {url}...")
    cap = cv2.VideoCapture(url)
    
    if not cap.isOpened():
        print("[Video]: Error: Unable to open camera stream.")
        return None
        
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("[Video]: Error: Failed to capture image from stream.")
        return None
        
    image_path = "snapshot.jpg"
    cv2.imwrite(image_path, frame)
    print(f"[Video]: Image saved to {image_path}")
    return image_path

# ==============================================================================
# --- AI ANALYSIS FUNCTION ---
# ==============================================================================

def analyze_with_gemini(image_path, client):
    """
    Uses Google Gemini Pro Vision to analyze an image and detect a human.
    
    Args:
        image_path (str): The file path to the image to be analyzed.
        client (genai.Client): The initialized Gemini client.
    
    Returns:
        bool: True if a human is detected, False otherwise.
    """
    if not os.path.exists(image_path):
        print(f"[AI]: Error: Image file not found at {image_path}")
        return False
        
    print(f"[AI]: Uploading {image_path} to Gemini for analysis...")
    try:
        img = Image.open(image_path)
        
        # This prompt is engineered to get a simple YES/NO answer
        prompt_text = (
            "Analyze this image from a home security sensor. "
            "Is there a real human, not any digital object, in this image? "
            "Respond with only the single word 'YES' or the single word 'NO'."
        )
        
        # Using a modern model for fast and accurate vision analysis
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[img, prompt_text]
        )
        
        result_text = response.text.strip().upper()
        print(f"[AI]: Gemini API Response: '{result_text}'")
        return result_text == "YES"
        
    except Exception as e:
        print(f"[AI]: Error during Gemini analysis: {e}")
        # Fail-safe: In case of API error, return False to avoid false alarms.
        return False

# ==============================================================================
# --- AUDIO ALERT FUNCTIONS ---
# ==============================================================================

# Initialize ElevenLabs Client
try:
    eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    print("[Audio]: ElevenLabs client initialized.")
except Exception as e:
    print(f"Error initializing ElevenLabs client: {e}")
    eleven_client = None

def generate_warning_audio(text_to_speak, filename="warning_audio.mp3"):
    """
    Generates an MP3 audio file from text using the ElevenLabs API.
    
    Args:
        text_to_speak (str): The text to synthesize into speech.
        filename (str): The name to save the audio file as.
    
    Returns:
        str or None: The absolute path to the saved audio file
                     or None if generation failed.
    """
    if not eleven_client:
        print("[Audio]: ElevenLabs client not initialized. Cannot generate audio.")
        return None
        
    print(f"[Audio]: Generating speech for: '{text_to_speak}'...")
    try:
        # Request audio stream from the API
        audio_stream = eleven_client.text_to_speech.convert(
            text=text_to_speak,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_multilingual_v2"
        )
        
        # Write the audio stream to a file
        with open(filename, "wb") as f:
            for chunk in audio_stream:
                if chunk:
                    f.write(chunk)
                    
        audio_path = os.path.abspath(filename)
        print(f"[Audio]: Audio file saved to {audio_path}")
        return audio_path
        
    except Exception as e:
        print(f"[Audio]: Error generating audio: {e}")
        return None

def play_audio_alert(audio_path):
    """
    Plays the specified audio file using playsound3.
    
    Args:
        audio_path (str): The file path of the audio to play.
    """
    if audio_path and playsound:
        print(f"[Audio]: Playing alert from {audio_path}...")
        try:
            playsound(audio_path)
            print("[Audio]: Alert playback finished.")
        except Exception as e:
            print(f"[Audio]: Error playing audio: {e}")
    elif not playsound:
        print("[Audio]: 'playsound3' library not found. Skipping playback.")
    else:
        print("[Audio]: No audio path provided. Skipping playback.")

# ==============================================================================
# --- MAIN EXECUTION (SYSTEM BRAIN) ---
# ==============================================================================

if __name__ == "__main__":
    
    # --- Step 1: Initialize Arduino Connection ---
    if platform.system() == "Windows":
        portVar = "COM5"  # Typical port for Windows
    else:
        # Adjust for your device on macOS or Linux
        portVar = "/dev/tty.usbserial-110" 
        
    serialInst = serial.Serial()
    serialInst.baudrate = SERIAL_BAUDRATE
    serialInst.port = portVar
    
    try:
        serialInst.open()
        print(f"[Serial]: Serial port {portVar} opened successfully.")
    except Exception as e:
        print(f"[Serial]: CRITICAL: Error opening serial port: {e}")
        print("Please check Arduino connection and port name (e.g., COM5).")
        exit()

    # --- Step 2: Initialize Gemini AI Client ---
    try:
        # NOTE: To test, users must create a .env file in the same directory
        # and add their key like this: GEMINI_API_KEY="YOUR_ACTUAL_KEY_HERE"
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")
        gemini_client = genai.Client(api_key=gemini_api_key)
        print("[AI]: Gemini client initialized successfully.")
    except Exception as e:
        print(f"[AI]: CRITICAL: Error initializing Gemini client: {e}")
        print("Please ensure your GEMINI_API_KEY is correct in the .env file.")
        exit()

    print("\n" + "="*30)
    print("AI SECURITY SYSTEM - ARMED AND READY")
    print(f"Listening for sensor signals on {portVar}...")
    print("="*30 + "\n")

    # --- Step 3: Start Main Sensor Loop ---
    while True:
        try:
            # Check if the Arduino has sent any data
            if serialInst.in_waiting:
                packet = serialInst.readline()
                serial_value = packet.decode('utf-8').strip()
                
                # Check for the specific trigger message from Arduino
                if "The value of pin is:" in serial_value:
                    value = serial_value.split(":")[-1].strip()
                    
                    # Sensor is triggered (LOW signal)
                    if value == '0':
                        print("\n--- [!!] SENSOR TRIGGERED [!!] ---")
                        
                        # --- PIPELINE STEP 1: CAPTURE IMAGE ---
                        image_file = capture_image_from_ipcam(IP_CAM_URL)
                        
                        if image_file:
                            # --- PIPELINE STEP 2: ANALYZE WITH AI ---
                            is_human = analyze_with_gemini(
                                image_file, gemini_client)
                                
                            if is_human:
                                # --- PIPELINE STEP 3: ALERT ---
                                print("\n*** [RESULT]: HUMAN DETECTED! ***")
                                print("--- Initiating Audio Alert ---")
                                text = "Warning: Unidentified human detected at the perimeter."
                                audio_path = generate_warning_audio(
                                    text, "warning_audio.mp3")
                                play_audio_alert(audio_path)
                                print("--- Alert Sequence Complete ---\n")
                            else:
                                print("\n*** [RESULT]: No Human Detected. (False Alarm) ***\n")
                        else:
                            print("[Error]: Failed to capture image, cannot perform analysis.")

        except serial.SerialException as e:
            print(f"CRITICAL: Serial connection lost: {e}. Exiting.")
            break
        except KeyboardInterrupt:
            print("\nShutdown signal received. Closing ports and exiting.")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")
            time.sleep(1) # Prevent rapid-fire error loops
            
        # Poll briefly to keep CPU usage low
        time.sleep(0.01)

    # Clean up connections on exit
    serialInst.close()
    print("Serial port closed. System shutdown.")