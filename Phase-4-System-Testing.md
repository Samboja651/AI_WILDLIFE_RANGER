# Phase 4: System Testing, Evaluation and Refinement

## Security measures in our system
1. The ml model
- the dataset is sourced from a google drive, has restricted sharing {confirm}
- the development environment (colab notebook) is restricted only to the devs.
- where did we originally download our dataset from, is it sourced ethically.
2. The codebase
- hosted on github on a private repository
- never commited env variables eg. api keys, db logins
- did not hardcode env values inside code.
- did client side and server side validation of form inputs

> try setting the min attribute using js.
> an authentication authorization mechanism to restrict unauthorized users.

## Fairness and Bias Evaluation
- fairness in ml It’s about creating algorithms and systems that treat individuals and groups equitably.
- Bias in ml refers to a systematic error or unfairness in the predictions or decisions made by a model
- I don't think fairness and bias apply for our model because we only focus on one lion. all prediction are based on that lion further more our model is more of a regressive rather than classification.

> implement explainable AI technique (SHAP) SHapley Additive exPlanations in our model----

## Sustainability Impact (Energy use and computational efficiency)
**Green computing practices.**
- we leverage cloud based solutions that is google maps javascrip api, google is on top for green energy {confirm this} and advocates for sustainable computing.
- used colab as development environment for the model. This helped to avoid the bandwidth cost of installing dependencies locally, or struggle to find computers with suitable hardware resources.

## System refinement based on feedback & ethical review
- our application can dynamically respond to all screen sizes {validate this}

> do more usability testing on UI

## Final Project Documentation & Ethical Reflection
**shall write the following**\
**Final Documentation Components:**
1. System Testing Report:
- Security assessment results.
- Fairness & bias evaluation.
- Sustainability impact analysis.
2. Refined & Improved System:
- Changes made based on feedback.
- New security, fairness, and sustainability measures.
3. Final Ethical Reflection:
- Challenges faced in applying responsible computing principles.
- Trade-offs between performance and ethics.
- Key lessons learned about bias, security, accessibility, and sustainability.