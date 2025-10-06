# Step 3: Lex Bot - Automated Setup Guide

## 🚀 **What I Can Do vs What You Need to Do**

### ✅ **I've Prepared (Ready to Use):**
- LF1 Lambda function code (`lf1_lex_fulfillment.py`)
- Deployment package (`lf1_lambda_function.zip`)
- Complete setup guide (`lex-bot-setup-guide.md`)
- All sample utterances and intents defined

### 🔄 **You Need to Do (AWS Console):**
Since your IAM user has limited permissions, you'll need to use the AWS Console for:

1. **Create LF1 Lambda Function**
2. **Create Lex Bot**
3. **Configure Intents**
4. **Integrate Lambda with Lex**

## 📋 **Quick Console Steps (15 minutes):**

### **Step 1: Create LF1 Lambda Function**
1. **AWS Console → Lambda → Create function**
2. **Name:** `LF1-LexFulfillment`
3. **Runtime:** Python 3.9
4. **Copy code from:** `lf1_lex_fulfillment.py`
5. **Click Deploy**

### **Step 2: Create Lex Bot**
1. **AWS Console → Amazon Lex**
2. **Create → Custom bot**
3. **Name:** `PantryPalBot`
4. **Language:** English (US)
5. **Click Create**

### **Step 3: Add 3 Intents (Copy-Paste Ready)**

#### **Intent 1: GreetingIntent**
- **Sample utterances:**
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

#### **Intent 2: ThankYouIntent**
- **Sample utterances:**
```
Thank you
Thanks
Thank you very much
Thanks a lot
Much appreciated
I appreciate it
```

#### **Intent 3: ServiceRequestIntent**
- **Sample utterances:**
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

### **Step 4: Integrate Lambda**
1. **For each intent → Fulfillment**
2. **Select:** AWS Lambda function
3. **Choose:** `LF1-LexFulfillment`
4. **Save Intent**

### **Step 5: Build & Test**
1. **Click "Build"** (wait 1-2 minutes)
2. **Click "Test"**
3. **Try:** "Hello" → Should get greeting response

## 🎯 **Expected Results:**

### **Test Phrases:**
- **"Hello"** → "Hello! I'm PantryPal, your culinary assistant. What ingredients do you have today?"
- **"Thank you"** → "You're welcome! I'm here to help you create amazing meals. What ingredients would you like to work with?"
- **"I need help with cooking"** → "Great! I can help you with ingredients in your kitchen. What specific ingredients do you have available? I'll suggest some delicious recipes!"

## 🔗 **Integration with Existing System:**

Once Lex is working, we can update your existing API Gateway to use Lex instead of the simple echo:

```javascript
// Updated LF0-ChatHandler would call Lex:
const lexResponse = await lex.postText({
    botName: 'PantryPalBot',
    botAlias: '$LATEST',
    userId: 'user123',
    inputText: userMessage
}).promise();
```

## 📁 **Files Ready for You:**
- `lf1_lex_fulfillment.py` - Lambda function code
- `lf1_lambda_function.zip` - Deployment package
- `lex-bot-setup-guide.md` - Detailed guide
- `step3-automation.md` - This quick guide

## ⏱️ **Time Estimate:**
- **Console setup:** 15 minutes
- **Testing:** 5 minutes
- **Total:** 20 minutes

All the code and configuration is ready - just follow the console steps above!
