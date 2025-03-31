# System Design with Responsible Computing

## 1. Privacy by Design

```python3
Definition - Integrate privacy measures into system architecture from the outset rather than as an afterthought.
```

**Privacy as the Default Setting** - We do not share any interporated data generated in model development. Only authorized people can access this data. In addition we know that the application is sensitive and prone to misuse, therefore during the development we kept the code and documentation private on github.

We only collected data of lions in Tsavo National park. This area is a hotspot to HWC therefore the need to collect and analyze data from lions in the region.

## 2. Fairness & Bias Detection

```python3
Bias detection - Refers to identifying and mitigating unfair outcomes in computing system -> AI/ML
```

```python3
Fairness - Ensures that software and systems do not favor one group over another and treat all users equitably.
```

Implementation

`Device Bias` - The dataset used is from a gps collar device that is prone to downtimes and signal loss. This contributes to inconsistent data recording. `Solution`, We filled in the gaps by interporating the data to achieve a consistent timestamp and time interval. We compared the nature of interporated data against original dataset and difference was negligible.

## 3. Transparency

### Potential Bias

Some parts of the dataset had very wide gaps of time interval 721 hours and most parts had averagely 5 hours time interval. Performing interpolation on such wide gaps results into artificial data thus a potential biased prediction.

### Limitations

1. Interporation was done at a consistency of two hours time interval. Therefore the model predicts locations to the next two hours.

2. The dataset focuses on one Lion named `Kiboche` in Tsavo National Park. Therefore the model can neither work well for other Lions nor Lion Kiboche in another park.

3. `Feature Bias` - the model focusses on learning the Lion movement patterns based on coordinates and time. All other dataset features like temperature that influence the reason behind the movements are obstructed.

## 4. Accountability

Model Performance is displayed to the users on the application performance page.\
Documentation - To the best of our ability, we have documented our model and application.
  
## 5. Safety

**Protecting the lion** - The application with the embedded model is only accessible to rangers through their government ranger ids.\
**Model Performance** - This influences how users use it.

## 6. Reliability

**Model Stability**: Incase of downtime on the gps collar device, the model by default brings the data into consistency of two hour intervals through interpolation. This ensures consistent predictions.

## 7. Accuracy

**Ground Truth Validation**: After doing a prediction, we measure the accuracy by comparing the distance in meters (500) from the actual Lion location recorded by the device. After computation, we display this as a performace metric to end user on the performance page.
