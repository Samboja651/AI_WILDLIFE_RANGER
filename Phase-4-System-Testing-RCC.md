# Phase 4: System Testing, Evaluation and Refinement

## Security measures in our system

### The Prediction Model

- The dataset is sourced from a google drive, has restricted sharing {confirm}
- The development environment (colab notebook) is restricted only to the developers.
- Where did we originally download our dataset from, is it sourced ethically?

### The Codebase

- Hosted on github on a private repository.
- Never commited env variables eg. api keys, db logins.
- Did not hardcode env values inside code.
- Did client side and server side validation of form inputs
- Privacy by Design - we have not made any of our source code or documentation publicly available.

> Try setting the min attribute on the form input using js.
> An authentication authorization mechanism to restrict unauthorized users.

## Fairness and Bias Evaluation

```python3
Fairness in ml is about creating algorithms and systems that treat individuals and groups equitably.
Bias in ml refers to a systematic error or unfairness in the predictions or decisions made by a model.
```

I don't think fairness and bias apply for our model because we only focus on one lion. all prediction are based on that lion further more our model is more of a regressive rather than classification.

> Implement explainable AI technique (SHAP) SHapley Additive exPlanations in our model.

## Sustainability Impact (Energy use and computational efficiency)

### Green computing practices

- We leverage cloud based solutions, that is, google maps javascrip api. Google is on top for green energy ***confirm this*** and advocates for sustainable computing.
- Used colab as development environment for the model. This helped to avoid the bandwidth cost of installing dependencies locally, or struggle to find computers with suitable hardware resources.

## System refinement based on feedback & ethical review

Our application can dynamically respond to all screen sizes ***validate this***.

> Do more usability testing on UI.

## Final Project Documentation & Ethical Reflection

**We shall write the following**\
**Final Documentation Components:**

**System Testing Report:**

- Security assessment results.
- Fairness & bias evaluation.
- Sustainability impact analysis.

**Refined & Improved System:**

- Changes made based on feedback.
- New security, fairness, and sustainability measures.

**Final Ethical Reflection:**

- Challenges faced in applying responsible computing principles.
- Trade-offs between performance and ethics.
- Key lessons learned about bias, security, accessibility, and sustainability.
