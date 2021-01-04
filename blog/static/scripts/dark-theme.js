const darkThemeElm = document.getElementById('dark-theme');

const darkLabel = "dark-theme-label";
const darkTextLabel = "Sombre";
const lightTextLabel = "Clair";


window.addEventListener('load', function () {
  if (darkThemeElm) {
    initTheme();
    /*
    Gestionnaire d'evenement commutateur de thème
    */
    darkThemeElm.addEventListener('change', function () {
      resetTheme();
    });
  }
});

/*
Initialise le thème lorsque la page est chargé.
*/
const initTheme = () => {
  const isDarkTheme = localStorage.getItem('theme') !== null && localStorage.getItem('theme') === 'dark';
  darkThemeElm.checked = isDarkTheme;
  if(isDarkTheme === true) {
    document.body.setAttribute('data-theme', 'dark')
    document.getElementById(darkLabel).innerHTML = darkTextLabel
  } else {
    document.body.removeAttribute('data-theme');
    document.getElementById(darkLabel).innerHTML = lightTextLabel;
  }
}

/*
Change le thème lorsque l'utilisateur 
appuie sur le commutateur sur la page.
*/
const resetTheme = () => {
  if (darkThemeElm.checked) {
    document.body.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    document.getElementById(darkLabel).innerHTML = darkTextLabel;
  } else {
    document.body.removeAttribute('data-theme');
    localStorage.removeItem('theme');
    document.getElementById(darkLabel).innerHTML = lightTextLabel;
  }
}