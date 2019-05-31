let {PythonShell} = require('python-shell')


var cors = require('cors');
var express = require('express');
const formidable = require('formidable')
const fs = require('fs');

var router = express.Router();

var multer  = require('multer');
var upload = multer({ dest: 'input/' });

router.get('/', function(req, res, next) {
  res.render('image', { title: 'Express' });
});



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

  PythonShell.run('hyphae_detector_modified.py', options, function (err, results) {
    if (err) throw err;
    console.log(results);
  });

  // Renaming code - doable

});

module.exports = router;
