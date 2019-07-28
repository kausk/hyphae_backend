const uploadFileS3 =  require('./amazon.js');

let {PythonShell} = require('python-shell')
var cors = require('cors');
var express = require('express');


const fs = require('fs');

const path = require("path");


var multer  = require('multer');
var upload = multer({ dest: './public/uploads/' })

const pathToRoot = '/Users/ksk/hyphae_frontend';
const savedImgLocation = '/public/output.png';
// const savedFilePath = pathToRoot + savedImgLocation


const savedFileFolderPath = '/Users/ksk/hyphae_backend/processed/';
var router = express.Router();



// Referenced from https://medium.com/@mahesh_joshi/reactjs-nodejs-upload-image-how-to-upload-image-using-reactjs-and-nodejs-multer-918dc66d304c
const storage = multer.diskStorage({
  destination: function(req, file, cb){
    "./public/uploads/"
  },
  filename: function(req, file, cb){
     cb(null,"IMAGE-" + Date.now() + path.extname(file.originalname));
  }
});

router.post('/', upload.single('image'), (req, res, next) => {

    console.log('post request');
    var regex = ".*\/";

    const parent_dir = __dirname.match(regex)[0];
    const filename = parent_dir.concat(req.file.path);

    console.log(filename);
    let options = {
      args: [filename]
    };
  
    console.log('running python');
    PythonShell.run('hyphae_detector_modified.py', options, function (err, results) {
      if (err) throw err;
      console.log('results');
      console.log(results);
      
      const area = results[0];
      const filename = results[1];

      res.json({
        area: area,
        result_img_location: filename
      });
        
      /*
      const upload_url = uploadFileS3(filename);
      if (upload_url != -1) {
        console.log('successful');
        console.log(upload_url);
        res.json({
          area: area,
          result_img_location: upload_url
        });
      } else {
        console.log('error');
        res.status(500);
      }
      
      return uploadFileS3(filename)
        .then(result => {
          console.log('result img location');
          console.log(result);


        })
        .catch(error => {
          console.log('error');
          res.status(500);
      });
      */

    });
  
    // Delete created file and saved file
});

/*
router.get('/', function(req, res, next) {
  res.render('image', { title: 'Express' });
});


// Referenced from https://medium.com/@mahesh_joshi/reactjs-nodejs-upload-image-how-to-upload-image-using-reactjs-and-nodejs-multer-918dc66d304c
// Referenced https://flaviocopes.com/express-forms-files/
router.post('/', upload.any(), function(req, res, next) {

  if (req.files.length == 0) {
    res.status(400);
    res.render('Must upload an image');
  }


  
  // Referenced https://github.com/richardgirges/express-fileupload/tree/master/example

  let filename = req.files[0].filename
  let options = {
    args: [filename]
  };

  let result;
  PythonShell.run('hyphae_detector_modified.py', options, function (err, results) {
    if (err) throw err;
    console.log(results);
    result = results;
    console.log(savedFilePath);
    // res.sendFile(savedFilePath);
    res.json({
      area: result[0],
      location: savedFilePath // saved image location
    });
  });

  //
  // Renaming code - doable

});
*/

module.exports = router;