# Step 3: Build the Lex Bot - Complete Setup Guide

## 🤖 **Lex Bot Configuration**

### **Step 1: Create Lex V1 Bot**
1. **Go to AWS Console → Amazon Lex**
2. **Click "Create" → "Custom bot"**
3. **Bot Configuration:**
   - **Bot name:** `PantryPalBot`
   - **Language:** English (US)
   - **Output voice:** None (text only)
   - **Session timeout:** 5 minutes
   - **IAM role:** Create new role (Lex will create it automatically)
4. **Click "Create"**

### **Step 2: Create the 3 Required Intents**

#### **Intent 1: GreetingIntent**
1. **Click "Create Intent"**
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
4. **Click "Save Intent"**

#### **Intent 2: ThankYouIntent**
1. **Click "Create Intent"**
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
4. **Click "Save Intent"**

#### **Intent 3: ServiceRequestIntent**
1. **Click "Create Intent"**
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
5. **Click "Save Intent"**

### **Step 3: Create LF1 Lambda Function**
1. **Go to AWS Console → Lambda**
2. **Click "Create function"**
3. **Function name:** `LF1-LexFulfillment`
4. **Runtime:** Python 3.9
5. **Click "Create function"**
6. **Replace the code** with the content from `lf1_lex_fulfillment.py`
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
                   "lex:PostText",
                   "lex:PostContent"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

### **Step 5: Integrate Lambda with Lex**
1. **Go back to Lex Console**
2. **For each intent:**
   - Click on the intent
   - Scroll to "Fulfillment"
   - Select "AWS Lambda function"
   - Choose `LF1-LexFulfillment`
   - Click "Save Intent"

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

After Lex bot is working, you can integrate it with your existing API Gateway by:
1. **Updating LF0-ChatHandler** to call Lex instead of echoing
2. **Using Lex PostText API** to process user messages
3. **Returning Lex responses** through your API Gateway

## 📁 **Files Created:**
- `lf1_lex_fulfillment.py` - Lambda function for Lex fulfillment
- `lf1_lambda_function.zip` - Deployment package for Lambda
- `lex-bot-setup-guide.md` - This setup guide

## 🎯 **Next Steps:**
1. Follow the AWS Console steps above
2. Test each intent thoroughly
3. Once working, we can integrate Lex with your existing API Gateway
