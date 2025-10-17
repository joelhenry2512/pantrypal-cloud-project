# Fresh Start: Complete PantryPal Project Setup

## 🚀 **Clean Rebuild - Guaranteed to Work**

This guide will help you build a working PantryPal chatbot from scratch with clean, simple code.

## **Step 1: Create Lambda Function**

### **1.1: Create New Lambda Function**
1. **Go to AWS Console → Lambda**
2. **Click "Create function"**
3. **Configure:**
   - **Function name:** `PantryPal-Clean`
   - **Runtime:** Python 3.9
   - **Architecture:** x86_64
4. **Click "Create function"**

### **1.2: Add Lambda Code**
1. **Delete the default code**
2. **Copy and paste** the code from `lambda_clean.py`
3. **Click "Deploy"**

### **1.3: Test Lambda Function**
1. **Click "Test"**
2. **Create test event:**
   ```json
   {
     "body": "{\"message\": \"Hello\"}"
   }
   ```
3. **Click "Test"**
4. **Should return:** `{"response": "Hello! I'm PantryPal..."}`

## **Step 2: Create API Gateway**

### **2.1: Create New API**
1. **Go to AWS Console → API Gateway**
2. **Click "Create API"**
3. **Choose "REST API" → "Build"**
4. **Configure:**
   - **Protocol:** REST
   - **Create new API:** New API
   - **API name:** `PantryPal-API`
5. **Click "Create API"**

### **2.2: Create Resource and Method**
1. **Click "Actions" → "Create Resource"**
2. **Configure:**
   - **Resource Name:** `chatbot`
   - **Resource Path:** `/chatbot`
3. **Click "Create Resource"**
4. **Select `/chatbot` resource**
5. **Click "Actions" → "Create Method"**
6. **Select "POST"**
7. **Click the checkmark**

### **2.3: Configure Integration**
1. **Integration type:** Lambda Function
2. **Use Lambda Proxy integration:** ✅ (check this)
3. **Lambda Function:** `PantryPal-Clean`
4. **Click "Save"**
5. **Click "OK" when prompted**

### **2.4: Enable CORS**
1. **Select `/chatbot` resource**
2. **Click "Actions" → "Enable CORS"**
3. **Configure:**
   - **Access-Control-Allow-Origin:** `*`
   - **Access-Control-Allow-Headers:** `Content-Type`
   - **Access-Control-Allow-Methods:** `POST, OPTIONS`
4. **Click "Enable CORS and replace existing CORS headers"**

### **2.5: Deploy API**
1. **Click "Actions" → "Deploy API"**
2. **Deployment stage:** `[New Stage]`
3. **Stage name:** `dev`
4. **Click "Deploy"**
5. **Copy the Invoke URL** (looks like: `https://abc123def4.execute-api.us-east-1.amazonaws.com/dev`)

## **Step 3: Update Frontend**

### **3.1: Update JavaScript**
1. **Open `script_clean.js`**
2. **Find line 7:**
   ```javascript
   const apiGatewayUrl = 'YOUR_API_GATEWAY_URL_HERE';
   ```
3. **Replace with your actual API Gateway URL:**
   ```javascript
   const apiGatewayUrl = 'https://abc123def4.execute-api.us-east-1.amazonaws.com/dev';
   ```

### **3.2: Upload to S3**
1. **Go to AWS Console → S3**
2. **Click on your bucket:** `ece528-chatbot-pantrypal`
3. **Upload these files:**
   - `index_clean.html` → rename to `index.html`
   - `style_clean.css` → rename to `style.css`
   - `script_clean.js` → rename to `script.js`
4. **Make sure to replace the existing files**

## **Step 4: Test Complete System**

### **4.1: Test Website**
1. **Go to:** `http://ece528-chatbot-pantrypal.s3-website-us-east-1.amazonaws.com/`
2. **Type "Hello" and press Send**
3. **Should get response:** "Hello! I'm PantryPal. You said: Hello..."

### **4.2: Test Different Messages**
- **"Thank you"** → Should get thanks response
- **"I want to cook"** → Should get cooking response
- **"What ingredients"** → Should get ingredient response

## **Step 5: Troubleshooting**

### **If Website Shows Error:**
1. **Check API Gateway URL** in script.js
2. **Check Lambda function** is deployed
3. **Check API Gateway** is deployed to dev stage
4. **Check CORS** is enabled

### **If Lambda Shows Error:**
1. **Check Python syntax** (no indentation errors)
2. **Check function is deployed**
3. **Test with simple event**

### **If API Gateway Shows Error:**
1. **Check integration** is set to Lambda Function
2. **Check Lambda Proxy** is enabled
3. **Check CORS** is configured

## **Expected Results**

✅ **Website loads** with PantryPal interface
✅ **Typing "Hello"** returns personalized response
✅ **Different messages** get different responses
✅ **No console errors** in browser
✅ **Network requests** show 200 status

## **Files Created:**
- `index_clean.html` - Clean HTML
- `style_clean.css` - Clean CSS
- `script_clean.js` - Clean JavaScript with debugging
- `lambda_clean.py` - Simple, working Lambda function
- `fresh-start-guide.md` - This setup guide

This clean implementation is guaranteed to work! 🎉
