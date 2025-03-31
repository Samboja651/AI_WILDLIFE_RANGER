# Prototype Development and Ethical Evaluation

We desire to build an ethical application and here are some things we did.

[ML prediction model codebase](https://colab.research.google.com/drive/1eLzl6sPXAiUuNLhWkPMxFJgJbLa70__4?usp=sharing)

## Incremental prototype Development

Used Agile methodology in entire development.\
Testing was done at each phase before proceeding to the next phase in the development.

## Secure coding practices

Used a `.env` file and never committed to Github.\
Form data is validated both on client & server side before storage on database.\
Exception handling - (e.g use of the try-except block)

## Energy use and computational efficiency

We leverage **cloud based solutions**, that is, `google maps javascrip api`. Google is a **strong** advocate for sustainable computing.

Used `google colab` as it contains most ML developmet libraries thus eliminating need for downloading them. We also found no need to get a powerful machine for ML training, Colab was sufficient.

Wrote a `DRY - Don't Repeat Yourself` code through reusable functions.

## Conducting user testing and feedback collection

Show cased system to Instructors and fellow students.

### Recommendations made

Add an Authentication mechanism.\
Incorporate a way for system users to give feedback.\
Add alerts through sms and emailing.\
Enhance UI Layouts and text understandable by non techies.
  
## Ethical Risk mitigation strategies

User passwords are encrypted on storage to database.

We've implemented secure coding practices by not hardcoding sensitive credentials. Used `env file`.
