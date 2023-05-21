
## 1. **User Registration**

   **Description:** This use case describes the process of user registration in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has accessed the Mark Out app.
   - **Postconditions:** User has successfully registered an account.

   **Flow of Events:**

   1. User opens the Mark Out app.
   2. User selects the "Register" option.
   3. User provides necessary information such as name, email, and password.
   4. User submits the registration form.
   5. The system validates the user's information.
   6. The system creates a new user account.
   7. The system confirms the successful registration and redirects the user to the login page.
## 2. **User Login**

   **Description:** This use case describes the process of user login in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has a registered account in the Mark Out app.
   - **Postconditions:** User has successfully logged into their account.

   **Flow of Events:**

   1. User opens the Mark Out app.
   2. User selects the "Login" option.
   3. User enters their email and password.
   4. User submits the login form.
   5. The system validates the user's credentials.
   6. The system grants access to the user's account and redirects them to their personalized homepage.

## 3. **Search for Wrestling PPV**

   **Description:** This use case describes the process of searching for a specific wrestling PPV in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has logged into their account.
   - **Postconditions:** User has found the desired wrestling PPV.

   **Flow of Events:**

   1. User navigates to the search bar in the app.
   2. User enters the keywords or title of the desired wrestling PPV.
   3. User submits the search query.
   4. The system retrieves search results based on the query.
   5. User reviews the search results and selects the desired wrestling PPV.
   6. The system displays detailed information about the selected wrestling PPV, including event name, date, location, and card details.

## 4. **Add Match to Watch List**

   **Description:** This use case describes the process of adding a match to the user's watch list in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has logged into their account.
   - **Postconditions:** The selected match is added to the user's watch list.

   **Flow of Events:**

   1. User navigates to a match page or search results displaying the match.
   2. User selects the "Add to Watch List" option for the desired match.
   3. The system adds the match to the user's watch list and provides a confirmation message.
   4. User can now access the match from their watch list for easy reference.

## 5. **Customize Homepage Favorite List**

   **Description:** This use case describes the process of customizing the user's homepage favorite list in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has logged into their account.
   - **Postconditions:** The user's homepage favorite list is updated according to their preferences.

   **Flow of Events:**

   1. User navigates to their personalized homepage.
   2. User selects the "Customize Favorite List" option.
   3. User can add or remove items such as matches, shows,

 and wrestler profiles from their favorite list.
   4. User saves the changes.
   5. The system updates the user's homepage to reflect the customized favorite list.

## 6. **Receive Personalized Recommendations**

   **Description:** This use case describes the process of receiving personalized recommendations based on user preferences and viewing history in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has logged into their account and has a viewing history.
   - **Postconditions:** User receives personalized recommendations based on their preferences.

   **Flow of Events:**

   1. User navigates to the recommendations section in the app.
   2. The system analyzes the user's viewing history and preferences.
   3. The system generates personalized recommendations for matches, PPVs, wrestlers, or related content.
   4. User views and accesses the recommended items based on their interests.

## 7. **Rate and Provide Feedback on Content**

   **Description:** This use case describes the process of rating and providing feedback on shows, wrestlers, matches, and other related content in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has logged into their account.
   - **Postconditions:** User's rating and feedback are recorded for the selected content.

   **Flow of Events:**

   1. User navigates to the page of the content they want to rate and provide feedback for (e.g., a specific match, show, or wrestler).
   2. User selects the "Rate and Provide Feedback" option for the content.
   3. User selects a rating scale (e.g., star rating, thumbs up/down).
   4. User provides additional comments or feedback regarding the content.
   5. User submits the rating and feedback.
   6. The system records the user's rating and feedback for the selected content.
   7. The system may use the rating and feedback to influence recommendations and overall content rankings.

## 8. **Optimize Performance and Responsiveness**

   **Description:** This use case describes the process of optimizing the performance and responsiveness of the Mark Out app.

   - **Actor:** System Administrator/Development Team
   - **Preconditions:** Mark Out app is deployed and accessible.
   - **Postconditions:** The Mark Out app demonstrates improved performance and responsiveness.

   **Flow of Events:**

   1. System administrator/development team monitors the performance of the app regularly.
   2. System administrator/development team identifies areas where performance can be optimized (e.g., slow loading times, inefficient database queries).
   3. System administrator/development team analyzes the code and infrastructure to identify potential bottlenecks.
   4. System administrator/development team implements performance optimization techniques, such as caching, query optimization, and code refactoring.
   5. System administrator/development team conducts load testing to simulate high user traffic and identify any performance issues.
   6. System administrator/development team fine-tunes the app's infrastructure, scaling resources as needed to ensure responsiveness under high load.
   7. System administrator/development team continues to monitor and optimize performance on an ongoing basis.

## 9. **Enable Social Sharing Functionalities**

   **Description:** This use case describes the process of enabling social sharing functionalities in the Mark Out app.

   - **Actor:** User
   - **Preconditions:** User has logged into their account.
   - **Postconditions:** User can share content from the Mark Out app on social media platforms.

   **Flow of Events:**

   1. User navigates to the content they want to share (e.g., a specific match, show, or wrestler).
   2. User selects the "Share" option for the content.
   3. User chooses the desired social media platform (e.g., Twitter, Facebook, Instagram).
   4. User is redirected to the selected social media platform, with pre-populated content to share (e.g., a link to the content, a brief description).
   5. User reviews and edits the shared content if desired.
   6. User submits the shared content, posting it on the selected social media platform.

## 10. **Handle Changes in Internet Wrestling Database Structure**

 **Description:** This use case describes how the Mark Out app handles changes in the structure or layout of the Internet Wrestling Database website.

 - **Actor:** System Administrator/Development Team
 - **Preconditions:** Mark Out app is deployed and connected to the Internet Wrestling Database website for data scraping. 
 - **Postconditions:** The Mark Out app adapts to changes in the Internet Wrestling Database website structure and continues to retrieve accurate data.

	 **Flow of Events:**

    1. System administrator/development team monitors the Internet Wrestling Database website for any changes in structure or layout.
    2. System administrator/development team identifies changes that may affect the data scraping process.
    3. System administrator/development team modifies the web scraping mechanism to accommodate the changes.
    4. System administrator/development team conducts tests to ensure the modified web scraping mechanism retrieves accurate and up-to-date data.
    5. System administrator/development team deploys the updated scraping mechanism to the live environment.
    6. System administrator/development team continues to monitor the Internet Wrestling Database website for further changes and makes necessary adjustments as required.