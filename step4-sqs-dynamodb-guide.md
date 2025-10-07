# Step 4: Add SQS + DynamoDB Integration

## 🚀 **Complete Setup Guide for SQS and DynamoDB**

### **Part 1: Create SQS Queue**

#### **Step 1: Create Standard SQS Queue**
1. **Go to AWS Console → SQS**
2. **Click "Create queue"**
3. **Configure:**
   - **Type:** Standard
   - **Name:** `pantrypal-requests-queue`
   - **Visibility timeout:** 30 seconds (default)
   - **Message retention period:** 14 days (default)
   - **Delivery delay:** 0 seconds (default)
   - **Maximum message size:** 256 KB (default)
4. **Click "Create queue"**
5. **Copy the Queue URL** (you'll need this for Lambda)

#### **Step 2: Get Queue URL**
- **Queue URL format:** `https://sqs.us-east-1.amazonaws.com/123456789012/pantrypal-requests-queue`
- **Save this URL** - you'll need it for the Lambda function

### **Part 2: Create DynamoDB Table**

#### **Step 1: Create DynamoDB Table**
1. **Go to AWS Console → DynamoDB**
2. **Click "Create table"**
3. **Configure:**
   - **Table name:** `ChatbotData`
   - **Partition key:** `RequestID` (String)
   - **Sort key:** Leave empty
   - **Table class:** Standard
   - **Read/Write capacity:** On-demand
4. **Click "Create table"**
5. **Wait for table to be "Active"**

#### **Step 2: Verify Table Structure**
- **Primary key:** RequestID (String)
- **Attributes will be added automatically when items are inserted**

### **Part 3: Update Lambda Function**

#### **Step 1: Update LF1 Lambda Function**
1. **Go to AWS Console → Lambda**
2. **Open function:** `LF1-LexV2Fulfillment`
3. **Replace the code** with content from `lf1_enhanced_fulfillment.py`
4. **Update the SQS_QUEUE_URL** in the code with your actual queue URL
5. **Click "Deploy"**

#### **Step 2: Update Lambda Permissions**
1. **Go to Lambda → Configuration → Permissions**
2. **Click on the execution role**
3. **Add these policies:**
   - `AmazonSQSFullAccess`
   - `AmazonDynamoDBFullAccess`
   - (Or create custom policies with minimal permissions)

#### **Step 3: Custom Policy (More Secure)**
Create a custom policy with these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:SendMessage",
                "sqs:GetQueueAttributes"
            ],
            "Resource": "arn:aws:sqs:us-east-1:YOUR_ACCOUNT_ID:pantrypal-requests-queue"
        },
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:YOUR_ACCOUNT_ID:table/ChatbotData"
        }
    ]
}
```

### **Part 4: Test the Integration**

#### **Step 1: Test Lex Bot**
1. **Go to Lex V2 Console**
2. **Open your bot:** `PantryPalBot`
3. **Click "Test"**
4. **Try these phrases:**
   - "Hello" → Should store in DynamoDB and send to SQS
   - "Thank you" → Should process and queue
   - "I need help with cooking" → Should extract slots and queue

#### **Step 2: Verify SQS Messages**
1. **Go to SQS Console**
2. **Click on your queue:** `pantrypal-requests-queue`
3. **Click "Send and receive messages"**
4. **Click "Poll for messages"**
5. **You should see messages with RequestID, SessionID, Intent, etc.**

#### **Step 3: Verify DynamoDB Data**
1. **Go to DynamoDB Console**
2. **Click on table:** `ChatbotData`
3. **Click "Explore table items"**
4. **You should see records with:**
   - RequestID (primary key)
   - SessionID
   - Intent
   - ProductType
   - Location
   - Timestamp
   - Status

## 🧪 **Expected Results**

### **DynamoDB Records:**
```json
{
  "RequestID": "123e4567-e89b-12d3-a456-426614174000",
  "SessionID": "user123",
  "Intent": "ServiceRequestIntent",
  "ProductType": "chicken",
  "Location": "kitchen",
  "Timestamp": "2024-01-15T10:30:00.000Z",
  "Status": "Processing"
}
```

### **SQS Messages:**
```json
{
  "RequestID": "123e4567-e89b-12d3-a456-426614174000",
  "SessionID": "user123",
  "Intent": "ServiceRequestIntent",
  "ProductType": "chicken",
  "Location": "kitchen",
  "Timestamp": "2024-01-15T10:30:00.000Z"
}
```

## 🔧 **Troubleshooting**

### **Issue 1: "Access Denied" for SQS/DynamoDB**
- **Solution:** Add SQS and DynamoDB permissions to Lambda execution role
- **Check:** Role has `AmazonSQSFullAccess` and `AmazonDynamoDBFullAccess`

### **Issue 2: "Queue does not exist"**
- **Solution:** Update `SQS_QUEUE_URL` in Lambda function with correct URL
- **Check:** Queue URL format is correct

### **Issue 3: "Table does not exist"**
- **Solution:** Ensure DynamoDB table name is exactly `ChatbotData`
- **Check:** Table is in "Active" state

### **Issue 4: "Invalid JSON in SQS message"**
- **Solution:** Check Lambda function code for proper JSON serialization
- **Check:** All required fields are included in message

## 📊 **Architecture Benefits**

### **SQS Benefits:**
- **Reliability:** Messages are queued even if processing fails
- **Scalability:** Can handle high message volumes
- **Decoupling:** Separates message processing from response generation

### **DynamoDB Benefits:**
- **Fast Queries:** Quick access to request data
- **Scalability:** Automatically scales with usage
- **Persistence:** Data is stored permanently for analytics

## 🎯 **Next Steps**

After successful integration:
1. **Monitor SQS queue** for message processing
2. **Check DynamoDB** for stored request data
3. **Consider adding a message processor** to handle SQS messages
4. **Implement analytics** using DynamoDB data

## 📁 **Files Created:**
- `lf1_enhanced_fulfillment.py` - Enhanced Lambda function
- `step4-sqs-dynamodb-guide.md` - This setup guide
