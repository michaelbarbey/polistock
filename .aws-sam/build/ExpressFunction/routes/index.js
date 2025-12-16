import { Router } from 'express';
var router = Router();

/* GET home page. */
router.get('/api/message', (req, res) => {
  res.json({ message: 'Hello from the Express backend!' });
});

export default router;
