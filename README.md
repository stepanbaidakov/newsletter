# Email Newsletter Management Service

An application for managing email newsletter campaigns, recipients, messages, and email delivery attempts. The service allows users to create and manage mailing lists, schedule campaigns, send emails, track delivery results, and view statistics. It also provides user authentication, role-based access control, and caching to improve performance.

## Features

The application is designed to provide the following functionality:

- Create, view, edit, and delete email recipients.
- Manage email messages, including their subjects and content.
- Create, view, edit, and delete mailing campaigns.
- Associate messages and recipients with mailing campaigns.
- Validate campaign start and end times.
- Calculate mailing campaign statuses dynamically.
- Launch email campaigns manually through the application interface or command line.
- Record successful and unsuccessful email delivery attempts.
- Display dashboard statistics.
- Register and authenticate users, verify email addresses, and recover passwords.
- Provide user-specific statistics and reports.
- Restrict access according to user roles.
- Cache data to improve application performance.

## Architecture and Key Features

### Recipient Management

The recipient model stores the information required to send emails:

- **Email** — a unique email address.
- **Full name** — the recipient's full name.
- **Comment** — optional additional information.

Users can manage their own recipients, while managers can view recipients across the service.

### Message Management

The message model contains:

- **Subject** — the email subject.
- **Body** — the email content.

Messages can be associated with mailing campaigns and reused where appropriate.

### Mailing Campaign Management

Each mailing campaign contains:

- **Start time** — the earliest time at which the campaign can be sent.
- **End time** — the deadline for sending the campaign.
- **Status** — the current campaign status.
- **Message** — a foreign key referencing the message to send.
- **Recipients** — a many-to-many relationship with recipients.

Campaign start and end times are required. The start time must not be in the past when creating a campaign, and it must be earlier than the end time.

Campaign statuses are calculated dynamically based on the current time:

- **Created — the current time is earlier than&#x20;**`start_time`.
- **Launched — the current time is between&#x20;**`start_time` and `end_time`, inclusive.
- **Completed — the current time is later than&#x20;**`end_time`.

### Email Delivery

A campaign can be launched manually through the application interface.

Before sending emails, the service checks whether the current time falls within the campaign's permitted sending period. If the campaign is outside this period, the sending operation is rejected.

For each associated recipient, the application:

1. Sends the email using `send_mail()`.
2. Records the attempt time.
3. Stores the delivery status.
4. Saves the mail server response or error details.

### Mailing Attempt History

Each delivery attempt stores:

- **Attempt time — the date and time of the attempt.**
- **Status — successful&#x20;**&#x6F;&#x72;**&#x20;unsuccessfu**l.
- **Server response — the response from the mail server or error details.**
- **Mailing — a foreign key referencing the associated campaign.**

The attempt history supports delivery monitoring, reporting, and troubleshooting.

### Dashboard and Statistics

The home page displays key service metrics:

- Total number of mailing campaigns.
- Number of active campaigns.
- Total number of unique recipients.

An active campaign is one whose current status is started and whose permitted sending period includes the current time.

Additional statistics include successful and unsuccessful delivery attempts and the number of messages sent by a user.

### Authentication and Access Control

The service supports user registration, login, logout, email verification, and password recovery.

Two main roles are provided:

**User**

- Create, view, edit, and delete their own recipients and mailing campaigns.
- View statistics for their campaigns.

**Manager**

- View all recipients and mailing campaigns.
- View registered users.
- Block users.
- Disable mailing campaigns.
- Cannot edit or delete other users' data.

### Caching

Server-side and client-side caching are intended to reduce unnecessary requests and improve application responsiveness.

## Tech Stack

- Python
- Django
- Bootstrap
- PostgreSQL
- Django ORM
- HTML
- SMTP / Django email backend
- Redis cache backend
- `pytest`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/stepanbaidakov/newsletter
cd newsletter
```

### 2. Install Dependencies

If the project uses Poetry:

```bash
poetry install
```

To install dependencies without installing the project itself:

```bash
poetry install --no-root
```

Alternatively, if a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root, using `.env.`sample as a template.

Example configuration:

```dotenv
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@example.com
```

The exact environment variable names depend on the database and email backend your using. Adjust the example to match the implementation.

Keep credentials and secret keys private. Do not commit `.env` to the repository. Add it to `.gitignore`, and commit only a template containing placeholder values.

### 4. Configure the Database and Redis

#### 1. Configure PostgreSQL

Install and start PostgreSQL, then create a database and configure the connection settings.

Run database migrations:

```bash
poetry run python manage.py migrate
```

Create an administrator account:

```bash
poetry run python manage.py createsuperuser
```

#### 2. Start Redis

Redis is used as a cache backend to improve application performance.

**Option A: Start Redis using Docker**

If Docker is installed, run:

```bash
docker run -d --name newsletter-redis -p 6379:6379 redis:latest
```

Check that the Redis container is running:

```bash
docker ps
```

To stop Redis:

```bash
docker stop newsletter-redis
```

To start the existing container again:

```bash
docker start newsletter-redis
```

**Option B: Start Redis locally**

If Redis is installed on your system, start the Redis server:

```bash
redis-server
```

Check the connection:

```bash
redis-cli ping
```

If Redis is running correctly, the response should be:

```text
PONG
```

By default, Redis listens on `localhost:6379`. Make sure the Redis connection settings in the Django application match the running Redis instance.
### 5. Configure Email Delivery

Configure the SMTP server or another supported email backend in the project settings.

For a production environment, use valid mail server credentials and verify the sender address. Never commit email passwords or other secrets to version control.

## Running the Application

For a Django application, start the development server with:

```bash
poetry run python manage.py runserver
```

Open the local address displayed in the terminal, typically:

`http://127.0.0.1:8000/`

## Usage

After starting the application, users can:

1. Register and verify their email address.
2. Log in to the service.
3. Create and manage email recipients.
4. Create email messages.
5. Create mailing campaigns and select recipients.
6. Set the campaign's start and end times.
7. Launch an eligible campaign.
8. Review delivery attempts and campaign statistics.

Managers have access to service-wide recipient and campaign information, user management, user blocking, and campaign disabling.

## Security Considerations

- Store passwords and secret keys securely.
- Use environment variables for sensitive configuration.
- Verify email addresses during registration.
- Enforce authorization checks for all user-specific operations.
- Prevent users from modifying other users' data.
- Validate campaign dates before sending emails.
- Avoid exposing SMTP credentials and internal server errors.
- Use HTTPS and secure cookie settings in production.

## Project Goals

The goal of the project is to provide a convenient and reliable email newsletter management service with recipient and campaign management, controlled email delivery, delivery history, reporting, authentication, role-based access control, and performance optimization.
