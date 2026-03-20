// =========JavaScript================
let voiceQueue = [];
let speaking = false;
let selectedEnv = null;


// ============================================
// DOM ELEMENTS
// ============================================
const chatContainer = document.getElementById("chatContainer");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

const cpuValue = document.getElementById("cpuValue");
const memoryValue = document.getElementById("memoryValue");
const diskValue = document.getElementById("diskValue");
const envValue = document.getElementById("envValue");

const micIcon = document.getElementById("micIcon");
const listeningStatus = document.getElementById("listeningStatus");

// Welcome Screen Elements
const welcomeScreen = document.getElementById("welcomeScreen");
const dashboardContent = document.getElementById("dashboardContent");

// ============================================
// BROWSER DETECTION & COMPATIBILITY
// ============================================
function getBrowserInfo() {
    const userAgent = navigator.userAgent;
    let browser = "Unknown";
    let version = "Unknown";

    if (userAgent.indexOf("Firefox") > -1) {
        browser = "Firefox";
        version = userAgent.split("Firefox/")[1];
    } else if (userAgent.indexOf("SamsungBrowser") > -1) {
        browser = "Samsung Internet";
    } else if (userAgent.indexOf("Opera") > -1 || userAgent.indexOf("OPR") > -1) {
        browser = "Opera";
    } else if (userAgent.indexOf("Trident") > -1) {
        browser = "Internet Explorer";
    } else if (userAgent.indexOf("Edge") > -1) {
        browser = "Edge";
    } else if (userAgent.indexOf("Chrome") > -1) {
        browser = "Chrome";
    } else if (userAgent.indexOf("Safari") > -1) {
        browser = "Safari";
    }

    return { browser, version, userAgent };
}

// Check if device is mobile/tablet
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Check touch support
function hasTouchSupport() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

// Log browser info for debugging
const browserInfo = getBrowserInfo();
console.log(`VoiceOps AI - Browser: ${browserInfo.browser}, Mobile: ${isMobileDevice()}, Touch: ${hasTouchSupport()}`);

// ============================================
// WELCOME SCREEN HANDLING
// ============================================
let welcomeScreenDismissed = false;

function dismissWelcomeScreen() {
    if (welcomeScreenDismissed) return;
    
    welcomeScreenDismissed = true;
    
    // Fade out welcome screen
    welcomeScreen.style.transition = 'opacity 0.5s ease';
    welcomeScreen.style.opacity = '0';
    
    setTimeout(() => {
        welcomeScreen.style.display = 'none';
        
        // Show dashboard content
        dashboardContent.classList.remove('dashboard-content-hidden');
        dashboardContent.classList.add('dashboard-content-visible');
    }, 500);
}

// Click anywhere on welcome screen to dismiss
if (welcomeScreen) {
    welcomeScreen.addEventListener('click', dismissWelcomeScreen);
    
    // Any keyboard press dismisses welcome screen
    document.addEventListener('keydown', function handleKeyPress(e) {
        if (welcomeScreen && !welcomeScreenDismissed) {
            dismissWelcomeScreen();
            document.removeEventListener('keydown', handleKeyPress);
        }
    });
}

// ============================================
// CHAT FUNCTIONALITY
// ============================================

// Append chat bubble
function addChatBubble(sender, text) {

    const bubble = document.createElement("div");
    bubble.classList.add("chat-bubble", sender.toLowerCase());

    // Generate timestamp like WhatsApp
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (sender.toLowerCase() === "me") {
        bubble.innerHTML = `
            <div><strong>Me:</strong> ${text}</div>
            <div class="chat-time">${time}</div>
        `;
    } else {
        bubble.innerHTML = `
            <div><strong>Bot:</strong> ${text}</div>
            <div class="chat-time">${time}</div>
        `;
    }

    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Text to Speech
function speakText(text){

  voiceQueue.push(text);

  if(!speaking){
      speakNext();
  }

}

function speakNext(){

  if(voiceQueue.length === 0){
      speaking = false;
      return;
  }

  speaking = true;

  const text = voiceQueue.shift();

  const speech = new SpeechSynthesisUtterance(text);

  speech.onend = () => {
      speakNext();
  };

  speechSynthesis.speak(speech);
}

// Send message to backend
async function sendMessage(message) {

    if (!message.trim()) return;

    // Detect environment
    const envMatch = message.match(/\b(dev|qa|uat|prod)\b/i);

    if (envMatch) {
        selectedEnv = envMatch[0].toUpperCase();
    }

    envValue.textContent = selectedEnv ? selectedEnv : "None";

    addChatBubble("ME", message);

    try {

        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: message }),
        });

        if (!res.ok) throw new Error("Server error");

        const data = await res.json();

        addChatBubble("BOT", data.response);

        speakText(data.response);

        // ===============================
        // FIXED METRICS HANDLING
        // ===============================

        cpuValue.textContent =
            data.cpu !== null && data.cpu !== undefined
                ? `${data.cpu}%`
                : "--";

        memoryValue.textContent =
            data.memory !== null && data.memory !== undefined
                ? `${data.memory}%`
                : "--";

        diskValue.textContent =
            data.disk !== null && data.disk !== undefined
                ? `${data.disk}%`
                : "--";

    } catch (e) {

        addChatBubble("BOT", `Error: ${e.message}`);

        cpuValue.textContent = "--";
        memoryValue.textContent = "--";
        diskValue.textContent = "--";

    }

}

// ============================================
// EVENT LISTENERS
// ============================================

// Send button click
sendBtn.addEventListener("click", () => {
    sendMessage(chatInput.value);
    chatInput.value = "";
});

// Enter key to send
chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendBtn.click();
    }
});

// Clear button
clearBtn.addEventListener("click", () => {
    chatContainer.innerHTML = "";
    cpuValue.textContent = "--";
    memoryValue.textContent = "--";
    diskValue.textContent = "--";
    envValue.textContent = "None";
});

// Preset buttons
document.getElementById("btnDevCpu").addEventListener("click", () => {
    sendMessage("dev cpu");
});

document.getElementById("btnQaCpu").addEventListener("click", () => {
    sendMessage("qa cpu");
});

document.getElementById("btnProdMemory").addEventListener("click", () => {
    sendMessage("prod memory");
});

// ============================================
// VOICE RECOGNITION SETUP - CROSS-BROWSER
// ============================================
let recognition;
let isListening = false;
let autoStopTimeout;

// Cross-browser Speech Recognition setup
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn("Speech Recognition not supported in this browser");
        if (micIcon) micIcon.style.display = "none";
        if (listeningStatus) {
            listeningStatus.textContent = "Voice Not Supported";
            listeningStatus.classList.add("red-text");
        }
        return false;
    }

    try {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-IN";
        recognition.maxAlternatives = 1;

        // Firefox specific settings
        if (browserInfo.browser === "Firefox") {
            recognition.lang = "en-US"; // Firefox has better support for en-US
        }

        // Safari specific settings
        if (browserInfo.browser === "Safari") {
            recognition.continuous = false;
        }

        recognition.onstart = () => {
            isListening = true;
            if (micIcon) {
                micIcon.classList.remove("red");
                micIcon.classList.add("green");
            }
            if (listeningStatus) {
                listeningStatus.textContent = "Listening...";
                listeningStatus.classList.remove("red-text");
                listeningStatus.classList.add("green-text");
            }
            console.log("Speech recognition started");
        };

        recognition.onend = () => {
            isListening = false;
            if (micIcon) {
                micIcon.classList.remove("green");
                micIcon.classList.add("red");
            }
            if (listeningStatus) {
                listeningStatus.textContent = "Not Listening";
                listeningStatus.classList.remove("green-text");
                listeningStatus.classList.add("red-text");
            }
            console.log("Speech recognition ended");
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log(`Voice input: ${transcript}`);
            sendMessage(transcript);
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            isListening = false;
            
            if (micIcon) {
                micIcon.classList.remove("green");
                micIcon.classList.add("red");
            }
            
            if (listeningStatus) {
                if (event.error === "no-speech") {
                    listeningStatus.textContent = "No Speech Detected";
                } else if (event.error === "audio-capture") {
                    listeningStatus.textContent = "Mic Access Denied";
                } else if (event.error === "not-allowed") {
                    listeningStatus.textContent = "Permission Denied";
                } else {
                    listeningStatus.textContent = "Error";
                }
                listeningStatus.classList.remove("green-text");
                listeningStatus.classList.add("red-text");
            }
            
            // Clear any pending timeout
            if (autoStopTimeout) {
                clearTimeout(autoStopTimeout);
            }
        };

        console.log("Speech recognition initialized successfully");
        return true;

    } catch (error) {
        console.error("Failed to initialize speech recognition:", error);
        if (micIcon) micIcon.style.display = "none";
        if (listeningStatus) {
            listeningStatus.textContent = "Voice Error";
            listeningStatus.classList.add("red-text");
        }
        return false;
    }
}

// Initialize speech recognition
const speechSupported = initSpeechRecognition();

// Mic click handler with cross-browser support
if (micIcon && speechSupported) {
    // Handle both click and touch events
    const micHandler = (e) => {
        e.preventDefault();
        
        if (isListening) {
            // Already listening, stop it
            if (recognition) {
                recognition.stop();
            }
            if (autoStopTimeout) {
                clearTimeout(autoStopTimeout);
            }
        } else {
            // Start listening
            try {
                recognition.start();
                
                // Auto stop after 5 seconds
                autoStopTimeout = setTimeout(() => {
                    if (recognition && isListening) {
                        recognition.stop();
                    }
                }, 5000);
                
            } catch (error) {
                console.error("Failed to start recognition:", error);
                // Reset UI state
                isListening = false;
                if (micIcon) {
                    micIcon.classList.remove("green");
                    micIcon.classList.add("red");
                }
                if (listeningStatus) {
                    listeningStatus.textContent = "Not Listening";
                    listeningStatus.classList.remove("green-text");
                    listeningStatus.classList.add("red-text");
                }
            }
        }
    };

    // Add click listener
    micIcon.addEventListener("click", micHandler);
    
    // Add touch listener for mobile devices
    if (hasTouchSupport()) {
        micIcon.addEventListener("touchstart", (e) => {
            e.preventDefault(); // Prevent default touch behavior
            micHandler(e);
        }, { passive: false });
    }
}

// ============================================
// PERMISSION CHECK FOR MICROPHONE
// ============================================
async function checkMicPermission() {
    try {
        if (navigator.permissions) {
            const result = await navigator.permissions.query({ name: 'microphone' });
            console.log(`Microphone permission: ${result.state}`);
            
            result.onchange = () => {
                console.log(`Microphone permission changed: ${result.state}`);
                if (result.state === 'denied') {
                    if (listeningStatus) {
                        listeningStatus.textContent = "Mic Permission Denied";
                        listeningStatus.classList.add("red-text");
                    }
                    if (micIcon) {
                        micIcon.style.opacity = "0.5";
                        micIcon.style.cursor = "not-allowed";
                    }
                }
            };
        }
    } catch (error) {
        console.warn("Could not check microphone permission:", error);
    }
}

// Check mic permission on load
checkMicPermission();

// ============================================
// LOGO CLICK - SHOW DASHBOARD
// ============================================
// The logo is already linked to "/" in base.html
// This ensures clicking the logo always shows the dashboard
console.log("VoiceOps AI Dashboard Loaded Successfully!");
console.log(`Ready for voice commands on ${browserInfo.browser}`);
// ============================================
// ALERT MONITORING
// ============================================

const alertToggle = document.getElementById("alertToggle");
let alertsEnabled = true;

if(alertToggle){
    alertToggle.addEventListener("change", () => {

        alertsEnabled = alertToggle.checked;

        const label = document.querySelector(".alert-label");

        if(alertsEnabled){
            label.textContent = "Alerts ON";
        }else{
            label.textContent = "Alerts OFF";
        }
    });
}


// popup alert
function showAlertPopup(text){

    const popup = document.createElement("div");
    popup.className = "alert-popup";
    popup.innerText = text;

    document.body.appendChild(popup);

    setTimeout(()=>{
        popup.remove();
    },5000);
}


// check alerts every 10 sec
async function checkAlerts(){

    if(!alertsEnabled) return;

    try{

        const res = await fetch("/api/alerts");

        const data = await res.json();

        if(data.alerts.length > 0){

          data.alerts.forEach(alert => {

            addChatBubble("BOT", alert);
        
            speakText(alert);
        
            showAlertPopup(alert);
        
          });

        }

    }catch(e){
        console.log("Alert check failed", e);
    }

}


// run every 10 seconds ONLY when dashboard open
if(window.location.pathname === "/"){

    setInterval(checkAlerts, 10000);

}