# Step 4: Configure Lambda Permissions for Lex V2

## 🔐 **Lambda Permissions Setup Guide**

### **Method 1: AWS Console (Recommended)**

#### **Step 1: Navigate to Lambda Function**
1. **Go to AWS Console → Lambda**
2. **Click on your function:** `LF1-LexV2Fulfillment`
3. **Click "Configuration" tab**
4. **Click "Permissions" in the left sidebar**

#### **Step 2: Access the Execution Role**
1. **Click on the execution role name** (it will be something like `LF1-LexV2Fulfillment-role-xxxxx`)
2. **This opens the IAM console for that role**

#### **Step 3: Add Lex V2 Permissions**
1. **Click "Add permissions" → "Attach policies"**
2. **Search for and select:** `AmazonLexV2FullAccess`
3. **Click "Add permissions"**

#### **Alternative: Create Custom Policy (More Secure)**
If you prefer a more restrictive policy, create a custom one:

1. **In IAM → Policies → Create policy**
2. **Use JSON editor and paste this policy:**

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lex:RecognizeText",
                "lex:RecognizeUtterance",
                "lex:GetSession",
                "lex:PutSession"
            ],
            "Resource": "*"
        }
    ]
}
```

3. **Name it:** `LexV2LambdaPermissions`
4. **Attach it to your Lambda execution role**

### **Method 2: AWS CLI (If you have permissions)**

```bash
# Get the role name first
aws lambda get-function --function-name LF1-LexV2Fulfillment --query 'Configuration.Role' --output text

# Attach the policy (replace ROLE_NAME with actual role name)
aws iam attach-role-policy --role-name ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonLexV2FullAccess
```

### **Method 3: Manual Policy Addition**

#### **Step 1: Find Your Lambda Role**
1. **In Lambda function → Configuration → Permissions**
2. **Copy the role ARN** (looks like: `arn:aws:iam::123456789012:role/LF1-LexV2Fulfillment-role-xxxxx`)

#### **Step 2: Go to IAM Console**
1. **AWS Console → IAM → Roles**
2. **Search for your role name** (from the ARN)
3. **Click on the role**

#### **Step 3: Add Policy**
1. **Click "Add permissions" → "Attach policies"**
2. **Search for:** `AmazonLexV2FullAccess`
3. **Select it and click "Add permissions"**

## 🧪 **Verify Permissions Work**

### **Test the Integration:**
1. **Go back to Lex V2 Console**
2. **Navigate to your bot:** `PantryPalBot`
3. **Go to each intent → Fulfillment**
4. **Select:** AWS Lambda function
5. **Choose:** `LF1-LexV2Fulfillment`
6. **Click "Save intent"**
7. **Build the bot**
8. **Test with:** "Hello" → Should work without permission errors

## ⚠️ **Common Issues & Solutions**

### **Issue 1: "Access Denied" Error**
- **Solution:** Make sure you attached `AmazonLexV2FullAccess` policy
- **Check:** Role has the policy attached in IAM console

### **Issue 2: "Function not found" in Lex**
- **Solution:** Make sure Lambda function name is exactly `LF1-LexV2Fulfillment`
- **Check:** Function exists and is deployed

### **Issue 3: "Invalid response format"**
- **Solution:** Make sure your Lambda function returns the correct Lex V2 response format
- **Check:** Use the `lf1_lex_v2_fulfillment.py` code exactly

## 📋 **Required Permissions Summary**

Your Lambda execution role needs these permissions:
- `lex:RecognizeText` - For processing user input
- `lex:RecognizeUtterance` - For voice input (if using)
- `lex:GetSession` - For session management
- `lex:PutSession` - For updating session state

## ✅ **Success Indicators**

You'll know it's working when:
- ✅ No permission errors in Lex console
- ✅ Lambda function can be selected as fulfillment
- ✅ Bot builds successfully
- ✅ Test conversations work without errors
- ✅ Intent responses come from your Lambda function

## 🔗 **Next Steps After Permissions**

Once permissions are configured:
1. **Integrate Lambda with all 3 intents**
2. **Build the Lex bot**
3. **Test each intent**
4. **Integrate with your existing API Gateway** (Step 5)

