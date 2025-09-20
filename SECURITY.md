# 🔒 Security Policy — NeoPaquet

## 📌 Supported Versions
We actively support and patch the following versions of **NeoPaquet**:

| Version     | Supported          |
|-------------|--------------------|
| v1.x.x      | ✅ Full support    |
| < v1.0.0    | ❌ No support      |

---

## 📢 Reporting a Vulnerability
If you discover a security vulnerability in **NeoPaquet**:

1. **Do not** publicly disclose the issue.  
2. Create a private report via **GitHub Security Advisories**:  
   👉 [NeoPaquet Security Advisories](https://github.com/JoeySoprano420/NeoPaquet/security/advisories)  
3. Alternatively, you may email the maintainers:  
   📧 **joeysoprano.dev@protonmail.com** (example — replace if you prefer another address).  

Please include:
- A clear description of the issue.  
- Steps to reproduce (if possible).  
- Potential impact (data leak, code execution, denial of service, etc.).  
- Suggested fix (if known).  

---

## 🛡️ Handling Process
- **Acknowledgment:** We will confirm receipt of your report within **48 hours**.  
- **Assessment:** Security team will evaluate severity (Low/Medium/High/Critical).  
- **Mitigation:** A fix or patch will be prepared and tested.  
- **Disclosure:** Coordinated disclosure will be made once the patch is released.  
- **Credit:** Reporters will be acknowledged (unless anonymity is requested).  

---

## 🔑 Best Practices for Users
- Always use the **latest release** of NeoPaquet.  
- Verify builds from GitHub Releases or PyPI (never use unverified binaries).  
- Run tests before deploying to production.  
- Review your **CIAM (Contextual Inference Abstraction Macros)** carefully — misconfigured macros may introduce vulnerabilities in compiled binaries.  
- Enable sandboxing when compiling untrusted code.  

---

## 📜 Legal Notice
NeoPaquet is licensed under the **[S.U.E.T. License v1.0](https://github.com/JoeySoprano420/NeoPaquet/blob/main/License.md)**.  
Security reports are handled in accordance with its sovereign and attribution clauses.  

---

Thank you for helping us keep **NeoPaquet** secure and reliable for everyone. 🙏
