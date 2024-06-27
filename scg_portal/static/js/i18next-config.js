// Set the initial language to English
let currentLanguage = 'en';
// Get the language button element
let languageButton = document.getElementById("language-button");

// Function to load the translation resources from the JSON files
async function loadResources(){
    // Fetch the English translation JSON file
    const enTranslation = await (await fetch('/static/js/locales/en/translation.json')).json();
    // Fetch the Spanish translation JSON file
    const esTranslation = await (await fetch('/static/js/locales/es/translation.json')).json();
    
    // Detect the language of the browser
    /**
    let browserLanguage = navigator.language.split("-")[0];
    if(browserLanguage === 'es' || browserLanguage === 'en'){
        currentLanguage = browserLanguage;
    }else{
        currentLanguage = 'en';
    }
    **/
    
    i18next.init({
        debug: true,
        lng: currentLanguage, // Set the current language
        resources: {
            en: {
                translation: enTranslation
            },
            es: {
                translation: esTranslation
            }
        },
        updateMissing: true, // Update missing translations
    });
}

// Function to update translations, including extended attributes
function updateTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (key.includes('[')) {
            // Handle extended attributes
            const parts = key.split(';');
            parts.forEach(part => {
                const match = part.match(/\[(.*?)\](.*)/);
                if (match) {
                    const attr = match[1];
                    const attrKey = match[2];
                    el.setAttribute(attr, i18next.t(attrKey));
                } else {
                    el.innerHTML = i18next.t(part);
                }
            });
        } else {
            // Regular translation
            el.innerHTML = i18next.t(key);
        }
    });
}

const SPAIN_FLAG = '<img src="/static/images/flags/spain-flag.png" alt="Spanish" class="flag-icon" >';
const UK_FLAG = '<img src="/static/images/flags/uk-flag.png" alt="English" class="flag-icon">';

// Modify the changeLanguage function
function changeLanguage() {
    if(currentLanguage === 'en') {
        i18next.changeLanguage('es', (err, t) => {
            updateTranslations();
        });
        currentLanguage = 'es';
        languageButton.innerHTML = UK_FLAG;
    } else {
        i18next.changeLanguage('en', (err, t) => {
            updateTranslations();
        });
        currentLanguage = 'en';
        languageButton.innerHTML = SPAIN_FLAG;
    }
    localStorage.setItem("currentLanguage", currentLanguage);
}

// Modify the loadResources().then() part
loadResources().then(() => {
    if(localStorage.getItem("currentLanguage")) {
        currentLanguage = localStorage.getItem("currentLanguage");
        i18next.changeLanguage(currentLanguage, (err, t) => {
            updateTranslations();
        });
        languageButton.innerHTML = currentLanguage === 'en' ? SPAIN_FLAG : UK_FLAG;
    } else {
        i18next.changeLanguage(currentLanguage, (err, t) => {
            updateTranslations();
        });
        languageButton.innerHTML = SPAIN_FLAG;
    }
});