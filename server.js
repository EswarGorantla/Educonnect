const express = require("express");
const cors = require("cors");
const path = require("path");
const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, "public"))); // To serve HTML
app.use("/uploads", express.static(path.join(__dirname, "uploads"))); // To serve uploaded videos

// Connect Routes
app.use("/api", require("./routes/api"));

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
