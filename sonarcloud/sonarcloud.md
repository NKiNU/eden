# SonarCloud Static Testing Report for Evidence-based Support Interface Evaluative Maintenance

## Overview
Definition of Evaluative Maintenance: In this type, common activities include reviewing the program code and documentations, examining the ripple effect of a proposed change, designing and executing tests, examining the programming support provided by the operating system, and finding the required data and debugging.


## Code Review Key Findings
### 1. Summary
| **Category**         | **Issues Identified** |
|----------------------|-----------------------|
| **Security**         | 12 vulnerabilities    |
| **Reliability**      | 3,000 issues          |
| **Maintainability**  | 58,000 code smells    |
| **Duplications**     | 6.6%                  |

![SonarCloud Summary](https://github.com/NKiNU/eden/tree/assignment1_nifailamsyar/sonarcloud/summary.png)



### 2. Issue Severity Breakdown
| **Severity**         | **Count** |
|----------------------|-----------|
| **Blocker**          | 434       |
| **High**             | 27,000    |
| **Medium**           | 27,000    |
| **Low**              | 6,400     |
| **Info**             | 0         |

### 3. Issue Type
| **Type**             | **Count** |
|----------------------|-----------|
| **Bug**              | 2,800     |
| **Vulnerability**    | 12        |
| **Code Smell**       | 58,000    |


![Breakdown](https://github.com/NKiNU/eden/tree/assignment1_nifailamsyar/sonarcloud/stats.png)

---

## Security Hotspots
### High Priority
- **Authentication Issues**: 367 hotspots.

### Medium Priority
- **Denial of Service (DoS)**: 254 hotspots.
- **Code Injection (RCE)**: 73 hotspots.
- **Weak Cryptography**: 53 hotspots.

### Low Priority
- **Encryption of Sensitive Data**: 3,914 hotspots.
- **Others**: 156 hotspots.

![Security Hotspots](https://github.com/NKiNU/eden/tree/assignment1_nifailamsyar/sonarcloud/security_hotspots.png)


---

## Benefits of Implementing SonarCloud Results
Implementing SonarCloud results offers several benefits, including enhanced security by addressing vulnerabilities and security hotspots, such as authentication flaws and weak cryptography. It also improves software reliability by resolving high and medium-severity issues, ensuring better stability and performance. Additionally, it promotes maintainable code by eliminating code smells, duplications, and inconsistencies, supporting long-term code health. Finally, it enables more targeted debugging, allowing teams to concentrate on critical areas, thus reducing time and effort spent on debugging.

---

## Conclusion
The SonarCloud analysis provides a clear roadmap for implementing **evaluative maintenance** by identifying key areas for improvement in **security**, **reliability**, and **maintainability**. By addressing the reported findings, the system can achieve higher stability, reduced technical debt, and improved code quality.
