# System Design with Responsible Computing

## Privacy by Design

```python3
Integrates privacy measures into system architecture from the outset rather than as an afterthought.
```

We have implemented **Privacy as the Default Setting**, how?  We do not share any interporated data generated in model development. Only authorized people can access this data. In addition we know that the application is sensitive and prone to misuse, therefore during the development we kept the code and documentation private on github.

We only collected data of lions in Tsavo National park. This area is a hotspot to HWC therefore the need to collect and analyze data from lions in the region.

> Does the application comply with data protection laws such as GDPR, HIPAA, or Kenya’s Data
Protection Act.

## Security by Design

```python3
Ensures security is built into systems from the beginning rather than later. 
```

> Implement one of `OWASP` coding standards. That is, ***solve*** [Security logging and monitoring failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/). ***Idea - log the print statements in our functions into .log file***.
>
> Implement a strong auth mechanis to meet another OWASP coding standards ***solve*** [Identificaiton and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
>
> Implemet `multi-factor-authentication` ***Idea - send confirmation codes to user email on registration***.

## Bias Detection

```python3
Refers to identifying and mitigating unfair outcomes in computing system -> AI/ML
```

I don't know if bias is a factor to our prediction model, but we should ask AI if a model such as ours can have what kind of biases?
In the algorithm, where we use geopy to calculate and check against the differential value. Can these be a form of `Algorithmic Bias`.

> Implement `explainable AI (XAI)` to increase transparecy.

## Fairness in Computing Systems

```python3
Ensures that software and systems do not favor one group over another and treat all users equitably.
```

> Implement Process fairness to show how decisions are made. ***Idea - document how we get report data***.

## Accesibility in Computing System
