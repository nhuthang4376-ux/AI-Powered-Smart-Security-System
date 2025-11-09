AI Powered Smart Security System
A sensor-based security system that integrates AI for real-time intrusion detection, image analysis, and voice alerts.

💡 Inspiration
We identified a key gap in the current smart home market: common security cameras cannot fully leverage the power of modern AI. Most "smart" cameras are closed systems, limited to basic, on-device algorithms (like simple motion vs. person detection) and are easily defeated by simple tactics (e.g., shining a bright light into the lens).

These systems lack the modularity to integrate with powerful, large-scale cloud AI for nuanced analysis or to execute a complex, proactive response. Our inspiration was to create a new solution: an "AI-centric" system that decouples simple hardware sensors from a powerful software "brain." This architecture allows us to use best-in-class cloud AI (like Google Gemini) for high-accuracy human verification and orchestrate a sophisticated, automated sequence of actions—from image capture to AI-generated voice warnings.

🧠 What We Learned
We learned many things during this project:

Team Cohesion: We learned how to build a stronger relationship within the team, making everyone work toward one big, shared goal.

Quick Learning: We learned the skill of learning fast to handle tasks we hadn't done before. This means understanding the general way things work, how to set them up, and how to fix errors, even if we don't know every tiny detail.

Time Management Under Pressure: We discovered how to manage our energy and focus over a 24-hour period. We realized the importance of short, planned breaks to keep our minds sharp and prevent making simple mistakes from exhaustion.

🛠️ How We Built the Project
We used a combination of hardware and software to build our system:

Hardware Setup: We used an Arduino board and various sensors (IR Break-beam Sensor, Limit Switch) to create the physical part of the project.

Code Languages: We wrote the code in C++ for the Arduino to send signals via the Serial port and used Python as the central "brain" to connect the hardware to the software logic.

AI Integration: We used external APIs to connect our project to AI services. This allowed us to:

Capture Image: Use OpenCV and Python to "hack" a phone into an IP Camera and capture a snapshot when a sensor is triggered.

Human Recognition: Send the snapshot to the Google Gemini Vision API (M4) to process the image and confirm if a real human is present.

Voice Warning: If a human is detected, the system calls the ElevenLabs API (M5) to generate an automatic voice warning and play it on the speakers.

😰 Challenges Faced
Our biggest challenge was lack of experience. As first-year students in our first hackathon, the amount of work was surprising. Most of the team had never used Arduino or worked with AI algorithms before, which meant we spent a lot of time just learning the basics.

However, because we worked together and helped each other learn new things, we managed to finish the project. We believe the core idea is strong, and we built the essential parts as well as we possibly could.

🏆 Accomplishments that we're proud of
The thing we are proudest of is that we successfully built our very first Arduino project and successfully integrated it with AI.

We built a complete processing pipeline from end-to-end: from the hardware sensor signal -> Python (PySerial) activation -> OpenCV image capture -> the image being sent to Gemini for analysis -> and finally, ElevenLabs generating a voice alert.

This is a complete project built with a lot of effort and hard work. Even though it has room for improvement, it is a project that truly belongs to us, and we are incredibly proud of it.

🚀 What's next for AI-Powered-Smart-Security-System
We see a bright future for our project. Our next steps would include:

Mobile Notifications: Integrating Blynk (M6) to send immediate push notifications and allow the user to arm/disarm the system remotely.

Automated Response: Enhancing the system to not only play a voice warning but also automatically make an emergency call (via Twilio - M5) and activate physical hardware like a Solenoid door lock (M5).

Power Optimization: Optimizing the Arduino code and hardware components to significantly reduce power consumption, allowing the system to run effectively on a small battery for extended periods.

Smart Home Integration: Creating APIs to allow the system to communicate with popular smart home platforms (like Google Home or Alexa) so the user can control the security system using voice commands.
