if (localStorage.getItem('targetedLanguage') != 'en') {

  let originalEnglishText = [];
  let translatedText = [];

  // Function to collect text from elements with data-translate attribute during initial page load
  function collectInitialText() {
      originalEnglishText = [];
      document.querySelectorAll('[data-translate]').forEach(element => {
          originalEnglishText.push(element.textContent);
      });
  }
  collectInitialText();
  
  function translateAllElements() {
    const selectedLanguage = localStorage.getItem('targetedLanguage');
    if (selectedLanguage === 'en') {
      window.location.reload()
    }
    sessionStorage.setItem('targetedLanguage', selectedLanguage);
    fetch('/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            texts: originalEnglishText,
            target_lang: selectedLanguage,
        }),
    })
    .then(response => response.json())
    .then(data => {
        translatedText = data.translated_texts || [];
        document.querySelectorAll('[data-translate]').forEach((element, index) => {
            element.textContent = translatedText[index] || '';
        });

    })
    .catch(error => {
        console.error('Translation error:', error);
    });
  }
  translateAllElements();
}

const hamMenuBtn = document.querySelector(".header__main-ham-menu-cont");
const smallMenu = document.querySelector(".header__sm-menu");
const headerHamMenuBtn = document.querySelector(".header__main-ham-menu");
const headerHamMenuCloseBtn = document.querySelector(
  ".header__main-ham-menu-close"
);
const headerSmallMenuLinks = document.querySelectorAll(".header__sm-menu-link");

hamMenuBtn.addEventListener("click", () => {
  if (smallMenu.classList.contains("header__sm-menu--active")) {
    smallMenu.classList.remove("header__sm-menu--active");
  } else {
    smallMenu.classList.add("header__sm-menu--active");
  }
  if (headerHamMenuBtn.classList.contains("d-none")) {
    headerHamMenuBtn.classList.remove("d-none");
    headerHamMenuCloseBtn.classList.add("d-none");
  } else {
    headerHamMenuBtn.classList.add("d-none");
    headerHamMenuCloseBtn.classList.remove("d-none");
  }
});
async function contactFormSubmission(form) {
  console.log(form.name.value);
  const params = {
    email: form.email.value,
    name: form.name.value,
    message: form.message.value,
  };
  const options = {
    method: "POST",
    body: JSON.stringify(params),
  };
  fetch("http://localhost:8080/upload-contact", {
    mode: "cors",
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(params),
  });
}
for (let i = 0; i < headerSmallMenuLinks.length; i++) {
  headerSmallMenuLinks[i].addEventListener("click", () => {
    smallMenu.classList.remove("header__sm-menu--active");
    headerHamMenuBtn.classList.remove("d-none");
    headerHamMenuCloseBtn.classList.add("d-none");
  });
}

const headerLogoConatiner = document.querySelector(".header__logo-container");

headerLogoConatiner.addEventListener("click", () => {
  location.href = "index.html";
});


