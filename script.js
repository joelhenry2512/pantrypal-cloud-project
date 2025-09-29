document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // !!! IMPORTANT !!!
    // REPLACE THIS URL WITH YOUR ACTUAL API GATEWAY ENDPOINT URL
    const apiGatewayUrl = 'https://z8im1nlcm2.execute-api.us-east-1.amazonaws.com/dev'; 

    // Display the initial welcome message from the bot
    displayMessage("Hi! I'm PantryPal. What ingredients do you have today?", 'bot');

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const userMessage = userInput.value.trim();
        
        if (userMessage) {
            displayMessage(userMessage, 'user');
            userInput.value = '';
            showTypingIndicator();
            await sendMessageToBot(userMessage);
        }
    });

    function displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to the latest message
    }
    
    function showTypingIndicator() {
        const typingElement = document.createElement('div');
        typingElement.classList.add('message', 'bot-message', 'typing-indicator');
        typingElement.id = 'typing-indicator';
        typingElement.textContent = 'PantryPal is thinking...';
        chatMessages.appendChild(typingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingElement = document.getElementById('typing-indicator');
        if (typingElement) {
            chatMessages.removeChild(typingElement);
        }
    }

    async function sendMessageToBot(userMessage) {
        if (apiGatewayUrl === 'YOUR_API_GATEWAY_URL_HERE') {
            removeTypingIndicator();
            displayMessage("Error: API Gateway URL is not configured. Please update it in script.js.", 'bot');
            return;
        }

        try {
            // Request body format for the Lambda function
            const requestBody = {
                message: userMessage
            };

            const response = await fetch(apiGatewayUrl + '/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }

            const responseData = await response.json();
            
            // Extract the response from the Lambda function
            const botResponse = responseData.response || "Sorry, I couldn't get a response.";
            
            removeTypingIndicator();
            displayMessage(botResponse, 'bot');

        } catch (error) {
            console.error('Error sending message to bot:', error);
            removeTypingIndicator();
            displayMessage("Sorry, I'm having trouble connecting. Please try again later.", 'bot');
        }
    }
});