# 4. Networking

### 1. Place the instances

Use three Amazon Linux 2023 EC2 instances in the same public subnet of the
default VPC. This avoids creating a VPC, subnet, internet gateway, and route
table. Enable auto-assigned public IPv4 addresses so the trainee can SSH
directly to each instance and install packages.

| Tier | Placement | Inbound access | Service port |
|---|---|---|---|
| Web | Public subnet | HTTP from internet; SSH from trainee's IP | 80 |
| App | Public subnet | SSH from trainee's IP; app traffic from Web SG | 5000 |
| DB | Public subnet | SSH from trainee's IP; DB traffic from App SG | 3306 |

### 2. Create and attach security groups

Create one security group per tier and set these inbound rules. In the AWS
console, choose **My IP** for each SSH rule; this limits remote shell access
to the trainee's current public IP.

- **Web:** TCP 80 from `0.0.0.0/0`; TCP 22 from My IP.
- **App:** TCP 22 from My IP; TCP 5000 from the Web security group.
- **DB:** TCP 22 from My IP; TCP 3306 from the App security group.

Attach each security group to its matching instance. The source security
group on ports 5000 and 3306 restricts app traffic to the intended tier;
never open these ports to the public internet. Use private IPs for
App-to-DB and Web-to-App traffic. Inbound access to the App and DB public IPs
is limited to SSH; the Web instance also accepts HTTP on port 80.

### 3. Understand the traffic path

Browser → Web public IP (port 80) → Nginx → App private IP (port 5000) → DB
private IP (port 3306).
