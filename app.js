const express = require('express');
const app = express();
const cors = require('cors');
const emailRoute = require('./routes/emailRoute');

app.use(cors()); // ✅ Important if frontend and backend are separate
app.use(express.json()); // ✅ To read JSON
app.use('/api', emailRoute); // ✅ To use /api/send-confirmation

app.listen(5000, () => {
  console.log("✅ Server running on http://localhost:5000");
});
