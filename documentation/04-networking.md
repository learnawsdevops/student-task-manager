# 4. Networking

Use three EC2 instances in the same public subnet of the default VPC. This
avoids creating a VPC, subnet, internet gateway, and route table. Enable
auto-assigned public IPv4 addresses so the trainee can SSH directly to each
instance and install packages.

| Tier | Placement | Inbound access | Service port |
|---|---|---|---|
| Web | Public subnet | HTTP from internet; SSH from trainee's IP | 80 |
| App | Public subnet | SSH from trainee's IP; app traffic from Web SG | 5000 |
| DB | Public subnet | SSH from trainee's IP; DB traffic from App SG | 3306 |

Create three security groups and set these inbound rules. In the console,
choose **My IP** for each SSH rule:

- **Web:** TCP 80 from `0.0.0.0/0`; TCP 22 from My IP.
- **App:** TCP 22 from My IP; TCP 5000 from the Web security group.
- **DB:** TCP 22 from My IP; TCP 3306 from the App security group.

Attach the matching security group to each instance. Do not add public inbound
rules for ports 5000 or 3306. Use private IPs for the App-to-DB and
Web-to-App connections; the public IPs are for SSH only.

Traffic path: Browser → Web public IP port 80 → Nginx → App private IP port
5000 → DB private IP port 3306.
