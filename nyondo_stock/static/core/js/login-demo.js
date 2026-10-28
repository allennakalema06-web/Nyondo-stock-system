"use strict";

const demoData = document.getElementById("demo-accounts");
if (demoData) {
  const accounts = JSON.parse(demoData.textContent);
  const username = document.getElementById("username");
  const password = document.getElementById("password");
  const status = document.getElementById("demo-status");
  document.querySelectorAll("[data-demo-index]").forEach((button) => {
    button.addEventListener("click", () => {
      const account = accounts[Number(button.dataset.demoIndex)];
      username.value = account.username;
      password.value = account.password;
      status.textContent = `${account.label} demo selected. Press Login to continue.`;
      username.focus();
    });
  });
}
