# SNS Email Notifications Troubleshooting Guide

## 🚨 **Issue: No Email Notifications Received**

### **Root Cause Analysis:**
The LF2 Lambda function is failing with error `'Records'` because it's not receiving the expected SQS event format.

## 🔧 **Step-by-Step Fix**

### **Step 1: Update LF2 Lambda Function**
1. **Go to AWS Console → Lambda**
2. **Open function:** `LF2-SQSProcessor`
3. **Replace the code** with content from `lf2_sqs_processor_fixed.py`
4. **Update SNS_TOPIC_ARN** with your actual topic ARN
5. **Click "Deploy"**

### **Step 2: Verify SQS Trigger Configuration**
1. **Go to Lambda → LF2-SQSProcessor**
2. **Click "Configuration" → "Triggers"**
3. **Check if SQS trigger exists:**
   - **Source:** SQS
   - **Queue:** `pantrypal-requests-queue`
   - **Status:** Enabled
4. **If no trigger exists:**
   - Click "Add trigger"
   - Select "SQS"
   - Choose your queue: `pantrypal-requests-queue`
   - Click "Add"

### **Step 3: Test SQS Trigger Manually**
1. **Go to SQS Console**
2. **Click on your queue:** `pantrypal-requests-queue`
3. **Click "Send and receive messages"**
4. **Send a test message:**
   ```json
   {
     "RequestID": "test-123",
     "SessionID": "test-session",
     "Intent": "GreetingIntent",
     "ProductType": "ingredients",
     "Location": "kitchen",
     "Timestamp": "2024-01-15T10:30:00.000Z"
   }
   ```
5. **Check LF2 Lambda logs** - should see processing

### **Step 4: Verify SNS Topic and Subscription**
1. **Go to SNS Console → Topics**
2. **Click on:** `ChatbotResponses`
3. **Check subscriptions:**
   - Should show your email
   - Status should be "Confirmed"
4. **If not confirmed:**
   - Check your email for confirmation link
   - Click the confirmation link

### **Step 5: Test Complete Flow**
1. **Go to Lex V2 Console**
2. **Test your bot** with "Hello"
3. **Check LF2 Lambda logs** for processing
4. **Check your email** for SNS notification

## 🧪 **Expected Log Output (Fixed)**

### **Successful Processing:**
```
Received event: {"Records": [{"messageId": "123", "body": "{\"RequestID\": \"abc123\"}"}]}
Processing record: 123
Processing request abc123 for intent GreetingIntent
Found DynamoDB record for abc123
Updated DynamoDB record abc123 to Processed
Published to SNS: 98765432-1234-5678-9012-123456789012
```

### **Error Handling:**
```
Received event: {"someOtherKey": "value"}
No 'Records' found in event. This might not be an SQS trigger.
Event keys: ['someOtherKey']
```

## 🔍 **Common Issues & Solutions**

### **Issue 1: "No 'Records' found in event"**
- **Cause:** SQS trigger not configured or wrong event source
- **Solution:** Add/verify SQS trigger configuration

### **Issue 2: "SNS_TOPIC_ARN not configured"**
- **Cause:** Topic ARN not updated in Lambda code
- **Solution:** Update SNS_TOPIC_ARN with actual ARN

### **Issue 3: "Access Denied" for SNS**
- **Cause:** Lambda execution role lacks SNS permissions
- **Solution:** Add `AmazonSNSFullAccess` policy to role

### **Issue 4: "Subscription not confirmed"**
- **Cause:** Email subscription not confirmed
- **Solution:** Check email and click confirmation link

### **Issue 5: "Topic does not exist"**
- **Cause:** Wrong SNS topic ARN
- **Solution:** Verify topic ARN in SNS console

## 📊 **Verification Checklist**

- ✅ LF2 Lambda function updated with fixed code
- ✅ SQS trigger configured and enabled
- ✅ SNS topic created and ARN updated in Lambda
- ✅ Email subscription confirmed
- ✅ Test message sent to SQS queue
- ✅ LF2 Lambda processes test message
- ✅ SNS notification received in email

## 🎯 **Next Steps After Fix**

1. **Test with real Lex bot** conversation
2. **Verify email notifications** are received
3. **Check DynamoDB** for updated records
4. **Monitor Lambda logs** for any remaining errors

## 📁 **Files Updated:**
- `lf2_sqs_processor_fixed.py` - Enhanced Lambda function with better error handling
- `sns-troubleshooting-guide.md` - This troubleshooting guide
