# 🏗️ Nyondo Stock System

A full-stack, role-based inventory, sales, supplier, and business management system built with **Django** for Nyondo General Hardware.

The system helps manage day-to-day hardware business operations including stock, products, suppliers, supplier credit, customers, sales, receipts, transport handling, reporting, and role-based access.

---

## 📌 Overview

**Nyondo Stock System** was developed for **Nyondo General Hardware LTD**, a wholesale and retail hardware business.

The application replaces manual record-keeping with a centralized digital system for managing business operations more accurately and efficiently.

It supports multiple user roles with different responsibilities:

- **Admin** — manages users, supplier credit, business records, and reports
- **Manager** — manages stock, products, suppliers, pricing, and inventory operations
- **Attendant** — records sales, issues receipts, and checks stock

The system is built with **Python, Django, PostgreSQL, HTML, CSS, and JavaScript**.

Production is deployed using **Vercel** with **Neon PostgreSQL** as the cloud database.

---

## 🌐 Live Demo

The production application is available here:

<p>
  <a href="https://nyondo-stock-system.vercel.app/">
    <img src="https://img.shields.io/badge/LIVE_DEMO-OPEN_APPLICATION-0B1220?style=for-the-badge&logo=vercel&logoColor=22D3EE" height="31" />
  </a>
</p>

### 🔐 Demo Access

The login page includes dedicated demo accounts for:

- Admin
- Manager
- Attendant

Visitors can use these accounts to explore the different role-based experiences.

> **Demo credentials are displayed directly on the application's login page.**

---

##  Features

### 📦 Inventory & Stock Management

- Product management
- Category management
- Stock registration
- Stock history
- Stock entry details
- Stock adjustments
- Low-stock monitoring
- Inventory tracking
- Product search and filtering
- Pagination

### 🤝 Supplier Management

- Supplier registration and management
- Supplier details
- Supplier credit tracking
- Supplier payment recording
- Outstanding supplier balance tracking

### 💰 Sales Management

- Multi-item sales
- Automatic stock updates
- Receipt generation
- Sales history
- Pending credit sales
- Transport handling
- Stock availability checks

### 👥 Customer Management

- Customer registration
- Customer records
- Customer sales information
- Support for business customer workflows

### 🚚 Transport Logic

The system includes business-specific transport rules for Nyondo General Hardware.

Eligible orders within the configured distance and order-value requirements receive free transport, while other qualifying deliveries can include a transport charge.

### 🛡️ Authentication & Role-Based Access

The application supports three primary roles:

- **ADMIN**
- **MANAGER**
- **ATTENDANT**

Each role receives access to the pages and operations relevant to its responsibilities.

### 📊 Reporting

- Reports dashboard
- Low-stock reporting
- Sales information
- Business activity visibility
- Revenue and operational records

### 👤 User Management

- User authentication
- User profiles
- Role assignment
- Group-based access control
- Permission-based route protection

---

## 🧰 Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| Frontend | HTML5, CSS3, JavaScript |
| Development Database | SQLite |
| Production Database | PostgreSQL, Neon |
| Deployment | Vercel |
| Static Files | WhiteNoise |
| Version Control | Git, GitHub |

---

## 🧱 Architecture

The project is organized into separate Django applications to keep business responsibilities modular.

```text id="36nwnf"
accounts_app
inventory_app
sales_app
customers_app
reports_app
core_app
```

These applications separate concerns such as authentication, inventory, sales, customers, reporting, and shared application functionality.

---

## 💻 Local Installation

### 1. Clone the repository

```bash id="1e4o1n"
git clone https://github.com/allennakalema06-web/Nyondo-stock-system.git
```

### 2. Navigate into the repository

```bash id="xfajey"
cd Nyondo-stock-system
```

### 3. Create a virtual environment

```bash id="igftai"
python -m venv venv
```

### 4. Activate the environment

#### Windows

```bash id="3djzsj"
venv\Scripts\activate
```

#### Git Bash on Windows

```bash id="77zu97"
source venv/Scripts/activate
```

#### Linux / macOS

```bash id="4speem"
source venv/bin/activate
```

### 5. Install dependencies

```bash id="0isocx"
pip install -r nyondo_stock/requirements.txt
```

### 6. Enter the Django project directory

```bash id="23ouid"
cd nyondo_stock
```

### 7. Configure environment variables

Create a `.env` file and configure the required values.

```env id="bvbz69"
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
ALLOWED_HOSTS=localhost,127.0.0.1
```

> ⚠️ Do not commit production credentials or secret keys to GitHub.

### 8. Run migrations

```bash id="jhk73z"
python manage.py migrate
```

### 9. Start the development server

```bash id="blfmyf"
python manage.py runserver
```

Then open:

```text id="7h7a17"
http://127.0.0.1:8000/
```

---

## ☁️ Production Deployment

The production architecture currently uses:

```text id="7l6fvn"
GitHub
   ↓
Vercel
   ↓
Django Application
   ↓
Neon PostgreSQL
```

The production database is hosted on **Neon PostgreSQL**, while the Django application is deployed through **Vercel**.

Environment variables such as the production database URL, secret key, allowed hosts, and trusted origins are configured securely in the deployment environment.

---

## 🧠 Skills Demonstrated

This project demonstrates experience with:

- Python
- Django
- Full-stack web development
- PostgreSQL
- Neon PostgreSQL
- Relational database design
- Authentication and authorization
- Django Groups and permissions
- Role-based access control
- Business logic implementation
- Inventory management systems
- Sales workflows
- Supplier-credit workflows
- Database migrations
- Production deployment
- Environment configuration
- Debugging
- Testing
- Git and GitHub workflows
- Software architecture
- Problem solving

---

## ⚙️ Business Rules Implemented

The application includes business-specific logic rather than functioning as a generic CRUD system.

Examples include:

- Supplier credit management
- Stock quantity updates
- Product pricing workflows
- Transport-charge decisions
- Sales receipts
- Pending credit sales
- Role-specific dashboards
- Stock adjustments
- Low-stock monitoring

These rules were designed around the actual operational requirements of Nyondo General Hardware.

---

## 🚀 Future Improvements

Potential future improvements include:

- REST API expansion
- More advanced analytics
- Visual sales and inventory dashboards
- Automated notifications
- Improved audit logging
- More comprehensive automated testing
- Exportable reports
- AI-assisted business insights
- Sales forecasting
- Intelligent stock recommendations

---

## ✅ Project Status

**Active and deployed**

The application is fully functional and publicly available for demonstration.

The current production version includes real role-based workflows, restored demonstration data, and dedicated public demo accounts for portfolio visitors.

---

## 🔗 Source Code

<p>
  <a href="https://github.com/allennakalema06-web/Nyondo-stock-system">
    <img src="https://img.shields.io/badge/SOURCE_CODE-VIEW_REPOSITORY-0B1220?style=for-the-badge&logo=github&logoColor=22D3EE" height="31" />
  </a>
</p>

---

##  Author

**Allen Nakalema**  
Software Engineer • AI Engineer

<p>
  <a href="https://allen-nakalema.pages.dev/">
    <img src="https://img.shields.io/badge/PORTFOLIO-VIEW_MY_WORK-0B1220?style=for-the-badge&logo=cloudflare&logoColor=22D3EE" height="31" />
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/allen-nakalema-99b8373aa/">
    <img src="https://img.shields.io/badge/LINKEDIN-CONNECT-0B1220?style=for-the-badge&logo=linkedin&logoColor=22D3EE" height="31" />
  </a>
  &nbsp;
  <a href="https://github.com/allennakalema06-web">
    <img src="https://img.shields.io/badge/GITHUB-VIEW_PROFILE-0B1220?style=for-the-badge&logo=github&logoColor=22D3EE" height="31" />
  </a>
</p>
