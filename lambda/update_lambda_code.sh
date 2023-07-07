

ZIP_FILE_NAME=lambda_function1.zip
INDEX_FILE_NAME=index.py
APP_DIR=app
S3_BUCKET=anycompany-personalize-lab
S3_KEY=qnabot-blog/lambda_function.zip
LAMBDA_FN_NAME=qna-Lambda
TARGET_REGION=us-east-1

# delete old index.py from zip file
echo "deleting index.py from zip file"
zip -d $ZIP_FILE_NAME "$INDEX_FILE_NAME"

# add new index.py to zip file
cd $APP_DIR
echo "adding new $INDEX_FILE_NAME to zip file $ZIP_FILE_NAME"
zip -g ../$ZIP_FILE_NAME $INDEX_FILE_NAME

# upload to s3 and update lambda function code
cd ..
echo "copying to S3 bucket"
aws s3 cp $ZIP_FILE_NAME s3://$S3_BUCKET/$S3_KEY
echo "updating lambda function code"
aws lambda update-function-code --function-name $LAMBDA_FN_NAME --s3-bucket $S3_BUCKET --s3-key $S3_KEY --region $TARGET_REGION