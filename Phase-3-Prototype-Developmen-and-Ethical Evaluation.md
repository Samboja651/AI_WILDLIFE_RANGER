# Phase 4: Prototype Development and Ethical Evaluation
## Incremental prototype Development
- Developed our system as small unit in each step allowing testing and making necessary adjustments that might be needed. 
- Testing was done at each phase before proceeding to the next phase in the development.
- The ml model used data for a single lion making it easy to train and test the model on other wildlife.

## Secure coding practices
- added the .env file that contains credentials that should not be not be exposed to the public( GitHub).
- Form data is validated before processing.
- Handled error within our app (e.g use of the try-except block)
- Regular testing of code for security flaws.

## Energy - Efficient Software/Hardware Usage
- used colab that has vast python libraries during our model development.
- Removed redundant code for better performance.

## Ethical AI/ML model training
- To do:
  1. use SHAP(Shapley Additive Explanation) for model transparency.
- fairness testing to detect biasses can't be achieved since we used data for for lions only and focused on one lion first.

## Conducting user testing and feedback collection
- To do:
  1. collect feedback from users by conducting a questionnaire(we should schedule a meeting with Victor, Leshan and Kantai).
  2.  conduct discussions with diverse users to asses inclusivity(we can do this hata kwa 'majirani').
  
## Ethical Risk mitigation strategies
  - On privary violation we can encrypt park ranger ID and the password for logins.
  - We've implemented secure coding practices by not hardcoding sensitive credentials.