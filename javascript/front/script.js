const ILength = document.querySelector("#length"),
  ISymbol = document.querySelector("#symbols"),
  INum = document.querySelector("#num"),
  btn = document.querySelector("button"),
  wrapper = document.querySelector(".passwords");

var passwords = [];

const printPasswords = () => {
  wrapper.innerHTML = passwords
    .map((item, index) => `<p>#${index + 1} password: ${item}</p>`)
    .join("");

  fetch("http://localhost:3000/passwords", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "http://localhost:3000/passwords",
    },
    body: JSON.stringify({
      passwords: passwords,
    }),
  })
    .then((res) => res.json())
    .then((res) => console.log(res));
};

const generatePassword = (len, sym, num) => {
  for (let i = 0; i < num; i++) {
    let str = "";
    for (let j = 0; j < len; j++) {
      str += sym.charAt(Math.floor(Math.random() * sym.length));
    }
    passwords.push(str);
  }
  printPasswords();
  console.log(passwords);
  passwords = [];
  return 0;
};

btn.addEventListener("click", () => {
  length = ILength.value;
  symbols = ISymbol.value;
  num = INum.value;

  length && symbols && num && generatePassword(length, symbols, num);
});
