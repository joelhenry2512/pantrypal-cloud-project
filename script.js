// Clean PantryPal Chatbot JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');

    // API Gateway URL - UPDATE THIS WITH YOUR ACTUAL URL
    const apiGatewayUrl = 'https://7alnh8dk1a.execute-api.us-east-1.amazonaws.com/dev';

    // Display welcome message
    displayMessage("Hi! I'm PantryPal. What ingredients do you have today?", 'bot');

    // Handle form submission
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
        chatMessages.scrollTop = chatMessages.scrollHeight;
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
        // Check if API Gateway URL is configured
        if (apiGatewayUrl === 'YOUR_API_GATEWAY_URL_HERE') {
            removeTypingIndicator();
            displayMessage("Error: API Gateway URL is not configured. Please update it in script.js", 'bot');
            return;
        }

        try {
            console.log('Sending message to:', apiGatewayUrl + '/chatbot');
            
            const response = await fetch(apiGatewayUrl + '/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: userMessage
                })
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('API Error:', errorText);
                throw new Error(`API request failed with status ${response.status}: ${errorText}`);
            }

            const responseData = await response.json();
            console.log('Response data:', responseData);
            
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
