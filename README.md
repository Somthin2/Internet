# Yugioh Search

## The site is also hosted at Somthin.pythonanywhere.com

#### General Idea of the Project

The project aims to create a site where anyone can search for their cards that they want and from there they can see its details and see its lowest available price.

## Templates

### api.html

This template is the page that will render the card searched.

### Duel.html

This template is only viewable once you logged in and its purpose is to be a calculator between a duel of two players. And if the LP ( Life Points ) of one goes to zero or below it announce the other one as the winner.
### Index.html

This is the main page where users can search the cards, also they are able to log in and register.

### Login.html

This is a basic login template that checks if the user entered the correct information. If everything is correct, the user can log in to their account.

### facebook.html

This template allows the user to log-in via facebook.

### MoreThings.html

This template has a few more things that where requested for the project such as cascaded backgrounds and real time videos.

### Register.html

This is a default register page where the user inputs their username, password, and confirms the password. An error is displayed if the user enters a username that was already registered in the database or if their password doesn't match the confirm password.

## Routes

### "/"

This is the main page that checks if there is an active user session. If not, it renders the "index.html" page. If there is an active user session, it checks if the user's profile and likings exist. If something doesn't exist, it renders the "FirstRegister.html" or "FirstLikings.html" page correspondingly. Finally, if everything is correct, it renders the home page when the user logs in.

### "/login"

This checks if the user didn't leave anything blank and if the username and password are correct. If everything is correct, the user's ID will be connected to the session["user_id"] value, and then the user will be redirected to the "/" route.

### "/register"

Firstly, the previous session is cleared so new values can be stored. Next, it checks for any errors the user can make. If the username the user entered hasn't been used already and the password matches the confirmation password, the user's info gets stored into the FireStore database. The session["user_id"] gets the user's ID, and then the user is redirected to "/".

### "/search"

This route uses a api from the ygoprodeck site and gets the response based on the card entered, if the card is found the response.status_code is equal to 200 hence we render all the information about the specific card, if not we render a png saying the card was not found.

### "/logout"

This route simply clears all the session data and then redirects the user to the "/" route.

### "/GetCards"

This route gets all the cards available and sends it to the html in a json file so it can be used as a list in the search bar.

### "/Duel"

This route renders the Duel html

