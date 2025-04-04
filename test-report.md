# Test Report for AI Wildlife Ranger

A detailed report of the testing process, results, and analysis for the AI Wildlife Ranger Flask application.

---

## 1. **Overview**

- **Application Name**: AI Wildlife Ranger
- **Testing Period**: 03/04/2025 - 04/04/2025
- **Testers**: Granton Waribe
- **Objective**: To validate the functionality, performance, usability, and security of the application.

---

## 2. Test Execution Results

### Summary of Test Execution

| **Test Case ID** | **Execution Status** | **Comments**                                                                 |
|------------------|----------------------|------------------------------------------------------------------------------|
| 1.1              | Passed               | User registration works as expected.                                        |
| 1.2              | Passed               | Error message displayed for duplicate registration.                         |
| 1.3              | Passed               | User login works with valid credentials.                                    |
| 1.4              | Passed               | Error message displayed for invalid credentials.                            |
| 2.1              | Passed               | Real-time location is fetched correctly.                                    |
| 2.2              | Passed               | Predicted location is accurate within acceptable limits.                    |
| 3.1              | Passed               | Email alert sent successfully.                                              |
| 3.2              | Failed               | SMS alert failed due to invalid Sinch API credentials.                      |
| S1               | Passed               | SQL injection attempt was blocked.                                          |
| S2               | Passed               | Restricted endpoints require login.                                         |
| S3               | Passed               | Passwords are hashed in the database.                                       |

---

## 3. **Test Case Execution Details**

### 3.1 Functional Testing

| **Test Case ID** | **Description**                              | **Status** | **Comments**                     |
|------------------|----------------------------------------------|------------|----------------------------------|
| 1.1              | Verify user registration with valid inputs.  | Passed | successful               |
| 1.2              | Verify error message for duplicate users.    | Passed | successful               |
| 1.3              | Verify user login with valid credentials.    | Passed | successful               |
| 1.4              | Verify error message for invalid credentials.| Passed | successful               |


### 3.2 Performance Testing

| **Test Case ID** | **Description**                              | **Status** | **Comments**                     |
|------------------|----------------------------------------------|------------|----------------------------------|
| 6.1              | Predict locations for 500 rows of data.      | Passed | on local machine, (my machine) it can serve 500 req one at a time for 7 minutes.               |
| 6.2              | Handle 50 concurrent user requests.          | Failed | limited skills              |

### 3.3 Usability Testing

| **Test Case ID** | **Description**                              | **Status** | **Comments**                     |
|------------------|----------------------------------------------|------------|----------------------------------|
| 7.1              | Verify navigation through the application.   | Passed | all links are working               |

### 3.4 Security Testing

| **Test Case ID** | **Description**                              | **Status** | **Comments**                     |
|------------------|----------------------------------------------|------------|----------------------------------|
| S1               | Test SQL injection on login form.            | Passed | client side validation  works             |
| S2               | Test access to restricted endpoints.         | Passed | redirects to login. user must login               |
| S3               | Verify password hashing in the database.     | Passed | encrypted-unreadbale text               |

---

## 4. **Bug Summary**

| **Bug ID** | **Description**                                   | **Severity** | **Status** | **Comments**                   |
|------------|---------------------------------------------------|--------------|------------|--------------------------------|
| B1         | Incorrect error message for duplicate registration.| Medium       | Open       | [Insert Comments]             |
| B2         | SMS notification fails with invalid credentials.  | High         | Open       | [Insert Comments]             |
| B3         | Feedback form lacks confirmation message.         | Low          | Open       | [Insert Comments]             |

---

## 5. **Performance Metrics**

| **Metric**                  | **Value**                        | **Remarks**                     |
|-----------------------------|-----------------------------------|----------------------------------|
| Average Response Time       | max 50seconds                   | hosting platform- render freemium service causes the high latency.                |
| Maximum Concurrent Requests | ?                   | limited skills                |
| Prediction Accuracy         | 58%                   | dependent on the dataset used                |

---

## 6. **Conclusion**

- **Overall Status**: Pass
- **Key Findings**:
  - if my free sinch api key runs out of usage, no sms are sent.
  - High Latency up to 50 sec. Render freemium service causes this. I noticed that the server shuts down when there is no activity therefore takes time to restart when a request is sent.
  - The register/login page are not responsive on small screens <600px
  - The map is poorly displayed on small screens
- **Recommendations**:
  - Since there is limited money, remoeve the sms notification feature when free api calls run out.
  - Use css media queries to make register/login & map mobile responsive
  - Create a python background worker that will run 24/7 sending one request every ten minutes to the render servive where the application is hosted. This will keep the server active preventing it from shutting down thus increasing response time. `From research: Render spins down a free web service that goes 15 minutes without receiving inbound traffic.`

---

- **Test Environment**:
  - **Operating System**: ubuntu 24.04
  - **Browser**: Google Chrome
  - **Database**: mysql & postgresql
  - **Postman**
  