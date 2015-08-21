#Core Client Tier

This is the client tier for the Braiiin application core.

##Purpose
The core is responsible for authentication and core services, such as account
management, privacy settings, and private spheres.

**Authentication Procedure**
All other Braiiin sites ask the core for a session ID by redirecting users
to the login page:

-   If the user is not logged in, show the login menu.
-   If the user is already logged in, and the next param is set, redirect the
    user to next, with the session ID. This gives other Braiiin websites the
    ability to then query its respective logic tier for user information.
    
    -   The next param must be within the braiiin.com or wocials.com domains.
    
-   If the user is already logged in, and the next param is not set, redirect
    the user to home.
    
