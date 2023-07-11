# This script will perform the following tasks:
#   1. Remove any old build files from previous runs.
#   2. Create a deployment S3 bucket to store build artifacts if not already existing
#   3. Installing required libraries and package them into ZIP files for Lambda layer creation. It will spin up a Docker container to install the packages to ensure architecture compatibility
#   4. Package the CloudFormation template and upload it to the S3 bucket

USAGE="$0 <cfn_bucket> <cfn_prefix> [public]"

BUCKET=$1
[ -z "$BUCKET" ] && echo "Cfn bucket name is required parameter. Usage $USAGE" && exit 1

PREFIX=$2
[ -z "$PREFIX" ] && echo "Prefix is required parameter. Usage $USAGE" && exit 1

# Remove trailing slash from prefix if needed
[[ "${PREFIX}" == */ ]] && PREFIX="${PREFIX%?}"

ACL=$3
if [ "$ACL" == "public" ]; then
  echo "Published S3 artifacts will be acessible by public (read-only)"
  PUBLIC=true
else
  echo "Published S3 artifacts will NOT be acessible by public."
  PUBLIC=false
fi

# define constants
DEPS_DIR=python
CURR_DIR=$PWD
LAYERS_DIR=$PWD/layers
LAMBDA_DIR=$PWD/lambda
BUILD_DIR=$PWD/build
REQS_TXT_PATH=requirements.txt
TEMPLATE_NAME=Bot-2023-06-06_v3
ECR_SAM_PYTHON_IMAGE=public.ecr.aws/sam/build-python3.10:1.90.0-20230706224408

echo "\n------------------------------------------------------------------------------"
echo "Remove any old build files from previous runs"
echo "------------------------------------------------------------------------------\n"
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR
mkdir -p $BUILD_DIR/layers


echo "\n------------------------------------------------------------------------------"
echo "Creating deployment S3 bucket if not exists and enabling ACLs if Public"
echo "------------------------------------------------------------------------------\n"


# Create bucket if it doesn't already exist
aws s3api list-buckets --query 'Buckets[].Name' | grep "\"$BUCKET\"" > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Creating S3 bucket: $BUCKET"
  aws s3 mb s3://${BUCKET} || exit 1
  aws s3api put-bucket-versioning --bucket ${BUCKET} --versioning-configuration Status=Enabled || exit 1
else
  echo "Using existing bucket: $BUCKET"
fi

# get bucket region for owned accounts
region=$(aws s3api get-bucket-location --bucket $BUCKET --query "LocationConstraint" --output text) || region="us-east-1"
[ -z "$region" -o "$region" == "None" ] && region=us-east-1;
echo "Bucket in region: $region"

if $PUBLIC; then
    echo "Enabling ACLs on bucket"
    aws s3api put-public-access-block --bucket ${BUCKET} --public-access-block-configuration "BlockPublicPolicy=false"
    aws s3api put-bucket-ownership-controls --bucket ${BUCKET} --ownership-controls="Rules=[{ObjectOwnership=BucketOwnerPreferred}]"
fi

echo "\n------------------------------------------------------------------------------"
echo "Creating Lambda Layers"
echo "------------------------------------------------------------------------------\n"
cd $LAYERS_DIR
echo "Docker run a container to build packages\n"
container_id=$(docker run -d -it -v $(pwd):/var/task $ECR_SAM_PYTHON_IMAGE)
for folder in */ ; do
    cd "$folder"
    layer_name=${PWD##*/}
    echo "Installing dependencies for $layer_name..."

    # removing any old files from previous runs
    rm -rf $DEPS_DIR
    mkdir -p $DEPS_DIR

    echo "Going to pip install dependencies listed in $folder$REQS_TXT_PATH"
    docker exec $container_id pip install -q -r $folder/$REQS_TXT_PATH --no-cache-dir --target=$folder/$DEPS_DIR

    # zip up the dependencies
    echo "Going to package dependencies into $BUILD_DIR/layers/$layer_name.zip"
    zip -r9 -q $BUILD_DIR/layers/$layer_name.zip $DEPS_DIR

    # upload layer ZIP file to S3 bucket
    echo "Uploading layer ZIP file to deployment bucket: s3://$BUCKET/$PREFIX/layers/$layer_name.zip"
    aws s3 cp $BUILD_DIR/layers/$layer_name.zip s3://$BUCKET/$PREFIX/layers/$layer_name.zip

    echo "Done installing dependencies for $layer_name!\n"

    cd $LAYERS_DIR
done

echo "Stopping the docker container"
docker stop $container_id

echo "\n------------------------------------------------------------------------------"
echo "Packaging CloudFormation artifacts"
echo "------------------------------------------------------------------------------\n"
cd $CURR_DIR
aws cloudformation package --template-file $TEMPLATE_NAME.yml --output-template-file $BUILD_DIR/$TEMPLATE_NAME-packaged.template --s3-bucket $BUCKET --s3-prefix $PREFIX --region ${region}|| exit 1

echo "Uploading packaged template $BUILD_DIR/$TEMPLATE_NAME-packaged.template to S3 bucket $BUCKET"
aws s3 cp $BUILD_DIR/$TEMPLATE_NAME-packaged.template s3://$BUCKET/$PREFIX/$TEMPLATE_NAME-packaged.template || exit 1

echo "Build done!\n"

echo "\n------------------------------------------------------------------------------"
echo "Validating CloudFormation artifacts"
echo "------------------------------------------------------------------------------\n"
template="https://s3.${region}.amazonaws.com/${BUCKET}/${PREFIX}/$TEMPLATE_NAME-packaged.template"
aws cloudformation validate-template --template-url $template > /dev/null || exit 1

echo "\n------------------------------------------------------------------------------"
echo "Outputs"
echo "------------------------------------------------------------------------------\n"
echo Template URL: $template
echo CF Launch URL: https://${region}.console.aws.amazon.com/cloudformation/home?region=${region}#/stacks/create/review?templateURL=${template}
echo CLI Deploy: aws cloudformation deploy --template-file $BUILD_DIR/$TEMPLATE_NAME-packaged.template --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --parameter-overrides deploymentS3BucketName=$BUCKET deploymentS3BucketPrefix=$PREFIX

echo "\nAll done!"
exit 0
