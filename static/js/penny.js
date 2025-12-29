document.getElementById("chatForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;

  const chatBox = document.getElementById("chatBox");


  const userBubble = document.createElement("div");
  userBubble.classList.add("message", "user-msg");
  userBubble.textContent = message;
  chatBox.appendChild(userBubble);
  chatBox.scrollTop = chatBox.scrollHeight;

  input.value = "";


  const thinkingBubble = document.createElement("div");
  thinkingBubble.classList.add("message", "bot-msg", "thinking");
  thinkingBubble.textContent = "Penny is thinking...";
  chatBox.appendChild(thinkingBubble);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("/get_penny_response", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();


    thinkingBubble.innerHTML = data.reply || "Sorry, I didn’t catch that.";
    thinkingBubble.classList.remove("thinking");

  } catch (error) {
    console.error("Fetch error:", error);
    thinkingBubble.textContent = "Penny encountered an error.";
    thinkingBubble.classList.remove("thinking");
  }

  chatBox.scrollTop = chatBox.scrollHeight;
});

