var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/api/message', (req, res) => {
  res.json({ message: 'Hello from Express backend!' });
});

module.exports = router;
