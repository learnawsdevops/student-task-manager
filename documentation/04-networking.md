# 4. Networking

Use three EC2 instances:

| Tier | Private subnet | Public access | Port |
|---|---|---|---|
| Web | Yes | Internet to TCP 80 | 80 |
| App | Yes | No public IP | 5000 from Web SG |
| DB | Yes | No public IP | 3306 from App SG |

Create these inbound rules:

- Web: TCP 80 from `0.0.0.0/0`; TCP 22 from the student's IP.
- App: TCP 5000 from the Web security group; TCP 22 from the student's IP.
- DB: TCP 3306 from the App security group; TCP 22 from the student's IP.

Traffic path: Browser → Web public IP port 80 → Nginx → App private IP port 5000 → DB private IP port 3306.

Use private IPs only for backend and database communication.
