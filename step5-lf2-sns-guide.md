# Step 5: Lambda LF2 + SNS Integration

## 🚀 **Complete Setup Guide for LF2 and SNS**

### **Part 1: Create LF2 Lambda Function**

#### **Step 1: Create LF2 Lambda Function**
1. **Go to AWS Console → Lambda**
2. **Click "Create function"**
3. **Configure:**
   - **Function name:** `LF2-SQSProcessor`
   - **Runtime:** Python 3.9
   - **Architecture:** x86_64
4. **Click "Create function"**

#### **Step 2: Add LF2 Code**
1. **Replace the default code** with content from `lf2_sqs_processor.py`
2. **Update the SNS_TOPIC_ARN** with your actual topic ARN (after creating SNS topic)
3. **Click "Deploy"**

#### **Step 3: Configure LF2 Permissions**
1. **Go to Lambda → Configuration → Permissions**
2. **Click on the execution role**
3. **Add these policies:**
   - `AmazonSQSFullAccess`
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`

### **Part 2: Create SNS Topic**

#### **Step 1: Create SNS Topic**
1. **Go to AWS Console → SNS**
2. **Click "Create topic"**
3. **Configure:**
   - **Type:** Standard
   - **Name:** `ChatbotResponses`
   - **Display name:** `PantryPal Bot`
4. **Click "Create topic"**
5. **Copy the Topic ARN** (you'll need this for Lambda)

#### **Step 2: Get Topic ARN**
- **Topic ARN format:** `arn:aws:sns:us-east-1:123456789012:ChatbotResponses`
- **Save this ARN** - you'll need it for the Lambda function

### **Part 3: Add SNS Subscription**

#### **Step 1: Create Email Subscription**
1. **Go to SNS Console → Topics**
2. **Click on your topic:** `ChatbotResponses`
3. **Click "Create subscription"**
4. **Configure:**
   - **Protocol:** Email
   - **Endpoint:** Your email address
5. **Click "Create subscription"**
6. **Check your email** and click the confirmation link

#### **Step 2: Create SMS Subscription (Optional)**
1. **Click "Create subscription"** again
2. **Configure:**
   - **Protocol:** SMS
   - **Endpoint:** Your phone number (with country code, e.g., +1234567890)
3. **Click "Create subscription"**

### **Part 4: Configure SQS Trigger for LF2**

#### **Step 1: Add SQS Trigger to LF2**
1. **Go to Lambda → LF2-SQSProcessor**
2. **Click "Add trigger"**
3. **Select:** SQS
4. **Configure:**
   - **SQS queue:** Select your `pantrypal-requests-queue`
   - **Batch size:** 1 (process one message at a time)
   - **Maximum batching window:** 0 seconds
5. **Click "Add"**

#### **Step 2: Update LF2 with SNS Topic ARN**
1. **Open LF2 Lambda function**
2. **Find this line:**
   ```python
   SNS_TOPIC_ARN = 'YOUR_SNS_TOPIC_ARN_HERE'
   ```
3. **Replace with your actual topic ARN:**
   ```python
   SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:ChatbotResponses'
   ```
4. **Click "Deploy"**

### **Part 5: Test the Complete Flow**

#### **Step 1: Test End-to-End Flow**
1. **Go to Lex V2 Console**
2. **Test your bot** with "Hello"
3. **Check the flow:**
   - ✅ Lex → LF1 → DynamoDB (store)
   - ✅ Lex → LF1 → SQS (queue)
   - ✅ SQS → LF2 (trigger)
   - ✅ LF2 → DynamoDB (query & update)
   - ✅ LF2 → SNS (notify)

#### **Step 2: Verify SNS Notifications**
1. **Check your email** for SNS notifications
2. **Check your phone** for SMS notifications (if configured)
3. **Messages should contain:**
   - Request ID
   - Intent information
   - Processed status
   - Bot response

#### **Step 3: Check DynamoDB Updates**
1. **Go to DynamoDB Console**
2. **Click on table:** `ChatbotData`
3. **Click "Explore table items"**
4. **Look for records with:**
   - `Status: "Processed"`
   - `ProcessedAt: timestamp`

## 🧪 **Expected Results**

### **SNS Email/SMS Message:**
```json
{
  "RequestID": "123e4567-e89b-12d3-a456-426614174000",
  "SessionID": "user123",
  "Intent": "GreetingIntent",
  "ProductType": "ingredients",
  "Location": "kitchen",
  "ProcessedAt": "2024-01-15T10:30:00.000Z",
  "Message": "Hello! Your greeting has been processed...",
  "Status": "Processed"
}
```

### **DynamoDB Record Updates:**
- **Status:** Changed from "Processing" to "Processed"
- **ProcessedAt:** Added timestamp
- **Original data:** Preserved

### **Lambda Logs (LF2):**
```
Processing request 123e4567-e89b-12d3-a456-426614174000 for intent GreetingIntent
Found DynamoDB record for 123e4567-e89b-12d3-a456-426614174000
Published to SNS: 98765432-1234-5678-9012-123456789012
```

## 🔧 **Troubleshooting**

### **Issue 1: "Topic does not exist"**
- **Solution:** Update SNS_TOPIC_ARN in LF2 with correct ARN
- **Check:** Topic ARN format is correct

### **Issue 2: "Access Denied" for SNS**
- **Solution:** Add SNS permissions to LF2 execution role
- **Check:** Role has `AmazonSNSFullAccess` policy

### **Issue 3: SQS trigger not working**
- **Solution:** Verify SQS trigger is configured correctly
- **Check:** Queue name matches exactly

### **Issue 4: No SNS notifications**
- **Solution:** Check email confirmation and subscription status
- **Check:** SNS topic has active subscriptions

## 📊 **Architecture Flow**

```
User → Lex → LF1 → DynamoDB (Store)
                ↓
              SQS (Queue)
                ↓
              LF2 (Process)
                ↓
              DynamoDB (Update)
                ↓
              SNS (Notify)
```

## 🎯 **Benefits Added**

### **LF2 Benefits:**
- **Message Processing:** Handles SQS messages asynchronously
- **Data Enrichment:** Queries DynamoDB for additional context
- **Status Tracking:** Updates request status to "Processed"

### **SNS Benefits:**
- **Notifications:** Users get notified of processed requests
- **Multiple Channels:** Email and SMS support
- **Reliability:** SNS ensures message delivery

## 📁 **Files Created:**
- `lf2_sqs_processor.py` - LF2 Lambda function
- `step5-lf2-sns-guide.md` - This setup guide
