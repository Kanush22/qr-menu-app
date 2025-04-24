# QR Code Menu App 🍽️

A web-based restaurant menu and order management system powered by QR codes and Streamlit.

## Project Overview

This application allows customers to view and place orders using a QR code placed on restaurant tables. The system provides:

- **Customer Interface:** Customers can scan a QR code to view the menu, add items to their cart, and place orders.
- **Admin Interface:** Admins (restaurant staff) can log in to manage the menu, view orders, and update order statuses.
- **Real-Time Menu Management:** Admins can update availability, add or remove items, and view orders in real-time.

## Features

- **For Customers:**
  - Scan QR code to open a table-specific menu.
  - Browse categorized menu items with descriptions and prices.
  - Add items to cart and place orders.
  - Provide special instructions for the kitchen (e.g., "no onions").
  
- **For Restaurant Admin:**
  - Manage the menu by adding, editing, or removing items.
  - Mark items as available or out of stock.
  - View orders with details such as table number, items, and special instructions.
  - Update order status (e.g., Received, In Progress, Served).
  
- **QR Code Generation:** Generate unique QR codes for each table.

## Technologies Used

- **Streamlit**: For building the interactive web application.
- **SQLite**: For storing menu items and orders.
- **Python**: Backend logic for the application.
- **qrcode**: To generate QR codes.

## Setup Instructions

### Prerequisites

- Python 3.x
- Streamlit

### Steps to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/qr-menu-app.git
   cd qr-menu-app
