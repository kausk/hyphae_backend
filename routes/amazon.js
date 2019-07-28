// Referenced https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-photo-album.html
// Referenced https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/s3-example-creating-buckets.html

var AWS = require('aws-sdk');
var fs = require('fs');
var path = require('path');

const BUCKET_NAME = 'images-hyphae';
const uploadParams = {Bucket: BUCKET_NAME, Key: '', Body: '', ACL:'public-read'};

// Create S3 service object
s3 = new AWS.S3({apiVersion: '2006-03-01'});

let uploadFileS3 = async filePath => {
    var fileStream = fs.createReadStream(filePath);
    fileStream.on('error', function(err) {
      console.log('File Error', err);
      return -1
    });
    uploadParams.Body = fileStream;
    uploadParams.Key = path.basename(filePath);

    let location;

    // call S3 to retrieve upload file to specified bucket
    return await s3.upload (uploadParams)
    /*
    , function (err, data) {
        if (err) throw err;
        console.log("Upload success", data);
        location = data.Location;
        return location;
    });    
    */
}


module.exports = uploadFileS3;