let isSpeaking = false;
let speechInstance;

// Function to handle text-to-speech
const handleSpeech = (textToSpeak) => {
  if ("speechSynthesis" in window) {
    if (isSpeaking) {
      window.speechSynthesis.cancel();
      isSpeaking = false;
    } else {
      window.speechSynthesis.cancel();
      speechInstance = new SpeechSynthesisUtterance(textToSpeak);
      speechInstance.lang = "en-US";
      speechInstance.volume = 1;
      speechInstance.rate = 1;
      speechInstance.pitch = 1;
      window.speechSynthesis.speak(speechInstance);
      isSpeaking = true;
    }
  }
};

// Function to toggle speech on button click
const toggleSpeech = () => {
  const botResponse = document.getElementById("resp").textContent.trim();
  if (botResponse) {
    handleSpeech(botResponse);
  }
};

// Function to send query
async function sendQuery() {
  const bot = document.getElementById("bot-select").value;
  const userInput = document.getElementById("user-input").value;

  if (!userInput) {
    alert("Please provide a query");
    return;
  }

  const responseDiv = document.getElementById("response");
  responseDiv.innerHTML = "Loading...";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ bot, userInput }),
    });

    const data = await response.json();
    responseDiv.innerHTML = `<strong>BOT:</strong> 
    <span id="resp">${data.answer}</span>`;

    // Enable Speak Button when response is received
    const speakButton = document.createElement("button");
    speakButton.type = "button";
    speakButton.className = "btn btn-sm btn-success speak-button";
    speakButton.textContent = "Speak";
    speakButton.onclick = toggleSpeech;

    responseDiv.appendChild(speakButton);
  } catch (error) {
    responseDiv.innerHTML = "Error: " + error.message;
  }
}

// Event listener for Enter key press in input field
document
  .getElementById("user-input")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendQuery();
    }
  });
