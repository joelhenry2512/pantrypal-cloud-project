# Step 3: Build the Lex V2 Bot - Updated Setup Guide

## ⚠️ **Important Update:**
Amazon Lex V1 is being deprecated (end of life September 15, 2025). We'll use Lex V2 instead.

## 🤖 **Lex V2 Bot Configuration**

### **Step 1: Create Lex V2 Bot**
1. **Go to AWS Console → Amazon Lex**
2. **Click "Create bot"** (V2 interface)
3. **Bot Configuration:**
   - **Bot name:** `PantryPalBot`
   - **Description:** `PantryPal Culinary Assistant Bot`
   - **IAM role:** Create new role (Lex will create it automatically)
   - **Data privacy:** Keep default settings
4. **Click "Create"**

### **Step 2: Create the 3 Required Intents**

#### **Intent 1: GreetingIntent**
1. **Click "Create intent"**
2. **Intent name:** `GreetingIntent`
3. **Sample utterances:**
   ```
   Hello
   Hi
   Hey
   Good morning
   Good afternoon
   Good evening
   Greetings
   How are you
   What's up
   ```
4. **Click "Save intent"**

#### **Intent 2: ThankYouIntent**
1. **Click "Create intent"**
2. **Intent name:** `ThankYouIntent`
3. **Sample utterances:**
   ```
   Thank you
   Thanks
   Thank you very much
   Thanks a lot
   Much appreciated
   I appreciate it
   ```
4. **Click "Save intent"**

#### **Intent 3: ServiceRequestIntent**
1. **Click "Create intent"**
2. **Intent name:** `ServiceRequestIntent`
3. **Sample utterances:**
   ```
   I need help with cooking
   What can I make with chicken
   I have rice and vegetables
   Help me with ingredients
   What should I cook
   I need recipe suggestions
   Can you help me cook
   What can I make for dinner
   ```
4. **Add Slots (optional but recommended):**
   - **Slot name:** `ProductType`
   - **Slot type:** AMAZON.Food
   - **Prompt:** "What type of food or ingredients are you working with?"
   
   - **Slot name:** `Location`
   - **Slot type:** AMAZON.City
   - **Prompt:** "Where are you cooking? (e.g., kitchen, home, etc.)"
5. **Click "Save intent"**

### **Step 3: Create LF1 Lambda Function (V2 Compatible)**
1. **Go to AWS Console → Lambda**
2. **Click "Create function"**
3. **Function name:** `LF1-LexV2Fulfillment`
4. **Runtime:** Python 3.9
5. **Click "Create function"**
6. **Replace the code** with the content from `lf1_lex_v2_fulfillment.py`
7. **Click "Deploy"**

### **Step 4: Configure Lambda Permissions**
1. **In Lambda function → Configuration → Permissions**
2. **Click on the execution role**
3. **Add this policy:**
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "lex:RecognizeText",
                   "lex:RecognizeUtterance"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

### **Step 5: Integrate Lambda with Lex V2**
1. **Go back to Lex V2 Console**
2. **For each intent:**
   - Click on the intent
   - Go to "Fulfillment"
   - Select "AWS Lambda function"
   - Choose `LF1-LexV2Fulfillment`
   - Click "Save intent"

### **Step 6: Build the Bot**
1. **Click "Build" button** (top right)
2. **Wait for build to complete** (usually 1-2 minutes)
3. **Status should show "Ready for testing"**

### **Step 7: Test the Bot**
1. **Click "Test" button**
2. **Try these test phrases:**
   - "Hello" → Should trigger GreetingIntent
   - "Thank you" → Should trigger ThankYouIntent
   - "I need help with cooking" → Should trigger ServiceRequestIntent
   - "What can I make with chicken" → Should trigger ServiceRequestIntent

## 🧪 **Testing Checklist**

### **Test GreetingIntent:**
- ✅ "Hello" → "Hello! I'm PantryPal, your culinary assistant..."
- ✅ "Hi there" → Should recognize as greeting
- ✅ "Good morning" → Should recognize as greeting

### **Test ThankYouIntent:**
- ✅ "Thank you" → "You're welcome! I'm here to help..."
- ✅ "Thanks a lot" → Should recognize as thanks
- ✅ "Much appreciated" → Should recognize as thanks

### **Test ServiceRequestIntent:**
- ✅ "I need help with cooking" → "Great! I can help you with ingredients..."
- ✅ "What can I make with chicken" → Should recognize as service request
- ✅ "I have rice and vegetables" → Should recognize as service request

## 🔗 **Integration with Existing System**

After Lex V2 bot is working, you can integrate it with your existing API Gateway by updating LF0-ChatHandler to use Lex V2:

```python
# Updated LF0-ChatHandler would call Lex V2:
lex_client = boto3.client('lexv2-runtime')
response = lex_client.recognize_text(
    botId='YOUR_BOT_ID',
    botAliasId='TSTALIASID',
    localeId='en_US',
    sessionId='user123',
    text=user_message
)
```

## 📁 **Files Created:**
- `lf1_lex_v2_fulfillment.py` - Lambda function for Lex V2 fulfillment
- `lex-v2-setup-guide.md` - This setup guide

## 🎯 **Next Steps:**
1. Follow the AWS Console steps above
2. Test each intent thoroughly
3. Once working, we can integrate Lex V2 with your existing API Gateway

## ⚠️ **Key Differences from V1:**
- Different event structure in Lambda
- Different API calls for integration
- Updated response format
- New console interface
