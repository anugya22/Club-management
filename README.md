# Club-management
A web-based application designed to streamline club activities, manage events, delegate tasks, track sales, and enhance communication between members, leads, and board members.

# Features:
User Roles and Authentication: Role-based access control with three user types: Members: Submit proposals, view tasks, and contact leads. Leads: Assign tasks, manage events, view member contributions, and track sales. Board Members: Oversee leads, manage events, view sales analytics, and contact other board members. Secure authentication using hashed passwords with Flask-Login.
Task Assignment: Leads can assign tasks to members, which are visible on their dashboards. Tasks can include descriptions and are organized by deadlines.
Event Management: Plan, update, and delete events for the club. View all upcoming and past events in a structured format.
Sales Tracking: Manage product sales and view a real-time pie chart of sales distribution. Add new products and track sales data for each product.
Member Contributions: Members can submit proposals, and leads can review them.
Communication Tools: Members can contact leads, and board members can communicate with each other. Email notifications (optional).
# Tech Stack:
Backend Python: Core programming language. Flask: Framework for routing and backend logic. SQLAlchemy: ORM for database operations. Frontend HTML5 and CSS3: Structure and styling. Bootstrap 5: Responsive design. JavaScript: Dynamic content updates. Database SQLite: Lightweight and easy-to-setup database. Others Flask-Mail: Email notifications. Matplotlib: Sales chart generation. dotenv: Secure environment variable management.

# Usage:
Create Users: Sign up users with different roles (Member, Lead, Board). Use the lead or board dashboards to manage tasks, events, and sales.
Assign Tasks: Leads can assign tasks to members, which will appear on the members’ dashboards.
Manage Events: Add, update, and view club events.
Track Sales View product sales analytics and add new products.
Monitor Member Contributions Review proposals submitted by members.
# Screenshots:
1. <img width="490" alt="image" src="https://github.com/user-attachments/assets/bf3e7b07-7b7a-4a1c-bffa-95c2122a8387" />


2.<img width="464" alt="image" src="https://github.com/user-attachments/assets/6c804024-b3ab-48fb-9468-d8856397057e" />


3.<img width="455" alt="image" src="https://github.com/user-attachments/assets/9599780d-2c38-4ef5-bbd6-84a615785bad" />


4.<img width="452" alt="image" src="https://github.com/user-attachments/assets/46b7ab3d-2345-4438-9355-dae13d816dbb" />


5.<img width="390" alt="image" src="https://github.com/user-attachments/assets/ea6cea2e-a7f6-4351-aba4-dc42f47827d2" />


6.<img width="428" alt="image" src="https://github.com/user-attachments/assets/aff62af4-d2c3-4d95-8000-b8c16e7f7918" />


7.<img width="434" alt="image" src="https://github.com/user-attachments/assets/a1b014f5-cf7d-460e-a207-233fc65bdff6" />


8.<img width="443" alt="image" src="https://github.com/user-attachments/assets/c530f7c2-9b27-40a3-ab33-5587c52678cc" />

9.<img width="445" alt="image" src="https://github.com/user-attachments/assets/2f75d4e8-65ad-4900-936f-084b4051a98d" />


# Testing:
Functional Testing Used Selenium to automate the testing of key user flows (e.g., task assignment, sales management).
Performance Testing Simulated 50 concurrent logins using JMeter to test server resilience. Contributing Fork the repository. Create a new branch: git checkout -b feature-name. Commit your changes: git commit -m "Add a new feature". Push to the branch: git push origin feature-name. Submit a pull request.
# Future Advancements
In the future, I plan to enhance my club management system to make it more general and adaptable for project management across various domains. This will involve integrating features such as MongoDB for efficient data handling, email notifications for seamless communication, scheduling meetings for better coordination, and team creation for structured collaboration. Additionally, I aim to implement file uploads and a dedicated work-related chat system to streamline project discussions. For scalability and reliability, I intend to deploy the system using AWS, ensuring a robust and efficient platform for managing projects beyond just clubs.
