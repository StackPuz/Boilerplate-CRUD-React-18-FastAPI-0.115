# Boilerplate-CRUD-React-18-FastAPI-0.115
Boilerplate CRUD Web App created with React 18 + FastAPI 0.115 by [StackPuz](https://stackpuz.com).

## Demo
Checkout the live demo at https://demo-spa.stackpuz.com

## Features
- Fully Responsive Layout.
- Sorting, Filtering and Pagination on Data List.
- User Management, User Authentication and Authorization, User Profile, Reset Password.
- Input Mask and Date Picker for date and time input field with Form Validation.

![Responsive Layout](https://stackpuz.com/img/feature/responsive.gif)  
![Data List](https://stackpuz.com/img/feature/list.gif)  
![User Module](https://stackpuz.com/img/feature/user.png)  
![Input Mask and Date Picker](https://stackpuz.com/img/feature/date.gif)

## Minimum requirements
- Node.js 14.18
- Python 3.10
- MySQL 5.7

## Installation
1. Clone this repository. `git clone https://github.com/stackpuz/Boilerplate-CRUD-React-18-FastAPI-0.115.git .`
2. Change directory to React project. `cd react`
3. Install the React dependencies. `npm install`
4. Change directory to FastAPI project. `cd ../fast_api`
5. Install the FastAPI project packages. `pip install -r requirements.txt`
6. Create a new database and run [/database.sql](/database.sql) script to create tables and import data.
7. Edit the database configuration in [/fast_api/config.json](/fast_api/config.json) file.

## Run project

1. Run React project. `npm run dev`
2. Run FastAPI project. `uvicorn app.main:app`
3. Navigate to `http://localhost:5173`
4. Login with user `admin` password `1234`

## Customization
To customize this project to use other Database Engines, CSS Frameworks, Icons, Input Mask, Date picker, Date format, Font and more. Please visit [stackpuz.com](https://stackpuz.com).

## License

[MIT](https://opensource.org/licenses/MIT)